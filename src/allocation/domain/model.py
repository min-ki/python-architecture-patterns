from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from . import events


# sqlalchemy 에러를 해결하기 위해서 unsafe_hash를 사용한다.
# https://github.com/cosmicpython/code/issues/17
@dataclass(unsafe_hash=True)  # frozen=True -> object cannot be modified. 즉, 불변 객체를 만든다.
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: set[OrderLine]

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        """__hash__ 매직 메서드는 집합에서 중복여부를 체크하거나 딕셔너리의 키로 사용할 때 사용된다."""
        return hash(self.reference)

    def __gt__(self, other: "Batch"):
        # eta가 없는 창고 재고를 먼저 사용해야한다.
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return (
            self.eta > other.eta
        )  # ex) 2023-05-29 > 2023-05-30 : 배송이 먼저 완료되는 것을 먼저 사용한다.

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate_one(self) -> OrderLine:
        return self._allocations.pop()

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


class OutOfStock(Exception):
    pass


class Product:
    def __init__(self, sku: str, batches: List["Batch"], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number
        self.events = []  # type: List[events.Event]

    def allocate(self, line: "OrderLine") -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            self.events.append(events.OutOfStock(sku=line.sku))
            return None

    def change_batch_quantity(self, ref: str, qty: int):
        batch = next(b for b in self.batches if b.reference == ref)
        batch._purchased_quantity = qty
        while batch.available_quantity < 0:
            line = batch.deallocate_one()
            self.events.append(
                events.AllocationRequired(
                    orderid=line.orderid, sku=line.sku, qty=line.qty
                )
            )
