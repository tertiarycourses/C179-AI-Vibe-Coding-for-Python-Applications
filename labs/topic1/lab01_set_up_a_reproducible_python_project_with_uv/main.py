# main.py
import pandas as pd

def main() -> None:
    df = pd.DataFrame({"card": ["4111...1111", "5500...0004", "4111...1111"],
                       "merchant": ["SG Grocer", "Overseas ATM", "SG Grocer"],
                       "amount": [42.90, 800.00, 15.50]})
    print(df)
    print(f"Total screened: ${df['amount'].sum():,.2f}")

if __name__ == "__main__":
    main()

