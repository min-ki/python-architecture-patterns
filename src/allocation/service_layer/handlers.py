from dataclasses import asdict
from typing import Callable, Dict, List, Type

from allocation.adapters import notifications
from allocation.domain import commands, events, model
from allocation.domain.model import OrderLine
from allocation.service_layer import unit_of_work
from sqlalchemy import text

from . import unit_of_work


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
    cmd: commands.CreateBatch,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=cmd.sku)
        if product is None:
            product = model.Product(cmd.sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(cmd.ref, cmd.sku, cmd.qty, cmd.eta))
        uow.commit()


def allocate(cmd: commands.Allocate, uow: unit_of_work.AbstractUnitOfWork) -> str:
    line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
        return batchref


def reallocate(
    event: events.Deallocated,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=event.sku)
        product.events.append(commands.Allocate(**asdict(event)))
        uow.commit()


def change_batch_quantity(
    cmd: commands.ChangeBatchQuantity,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get_by_batchref(batchref=cmd.ref)
        product.change_batch_quantity(ref=cmd.ref, qty=cmd.qty)
        uow.commit()


def send_out_of_stock_notification(
    event: events.OutOfStock,
    notifications: notifications.AbstractNotifications,
):
    notifications.send(
        "secreata77@gmail.com",
        f"Out of stock for {event.sku}",
    )


def publish_allocated_event(
    event: events.Allocated,
    publish: Callable,
):
    publish("line_allocated", event)


def add_allocation_to_read_model(
    event: events.Allocated,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            text(
                "INSERT INTO allocations_view (orderid, sku, batchref)"
                " VALUES (:orderid, :sku, :batchref)"
            ),
            dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref),
        )
        uow.commit()


def remove_allocation_from_read_model(
    event: events.Deallocated,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            text(
                "DELETE FROM allocations_view"
                " WHERE orderid = :orderid AND sku = :sku"
            ),
            dict(orderid=event.orderid, sku=event.sku),
        )
        uow.commit()


EVENT_HANDLERS = {
    events.Allocated: [publish_allocated_event, add_allocation_to_read_model],
    events.Deallocated: [remove_allocation_from_read_model, reallocate],
    events.OutOfStock: [send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.Allocate: allocate,
    commands.CreateBatch: add_batch,
    commands.ChangeBatchQuantity: change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]
