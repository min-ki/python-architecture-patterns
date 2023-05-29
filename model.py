
from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass(frozen=True) # frozen=True -> object cannot be modified. 즉, 불변 객체를 만든다.
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set() # type: set[OrderLine]


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
        if self.eta is None:
            return True
        return self.eta > other.eta # ex) 2023-05-29 > 2023-05-30 : 배송이 먼저 완료되는 것을 먼저 사용한다.

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

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

def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
