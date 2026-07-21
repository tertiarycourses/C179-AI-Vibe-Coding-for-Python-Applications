# Add a constructor that builds a Transaction from a database row
    @classmethod
    def from_row(cls, row: tuple) -> "Transaction":
        """Build a Transaction from a sqlite row tuple."""
        return cls(id=row[0], card_ref=row[1], ts=datetime.fromisoformat(row[2]),
                   amount=row[3], merchant_category=row[4], city=row[5],
                   lat=row[6], lon=row[7])

