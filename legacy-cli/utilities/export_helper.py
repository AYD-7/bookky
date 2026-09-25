import csv
import json
import os
from datetime import datetime


def filter_receipts_for_export(receipts_list: list[dict]) -> list[dict]:
    """Sub-menu to choose which receipts to export based on criteria."""
    if not receipts_list:
        print("No receipts available to export.")
        return []

    print("\n--- EXPORT FILTER MENU ---")
    print("1. All Receipts")
    print("2. Receipts in a Specific Month/Year")
    print("3. Receipts in a Specific Year")
    print("4. Receipts from a Category")
    print("5. Receipts from a Business")

    choice = input("Select an option (1-5): ").strip()

    # 1. All receipts
    if choice == "1":
        return receipts_list

    # 2. Month and Year
    elif choice == "2":
        try:
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year (e.g., 2026): "))
            filtered = []
            for r in receipts_list:
                dt = datetime.strptime(r["date"].strip(), "%d/%m/%Y")
                if dt.month == month and dt.year == year:
                    filtered.append(r)
            return filtered
        except ValueError:
            print("Invalid date inputs.")
            return []

    # 3. Year
    elif choice == "3":
        try:
            year = int(input("Enter year (e.g., 2026): "))
            filtered = []
            for r in receipts_list:
                dt = datetime.strptime(r["date"].strip(), "%d/%m/%Y")
                if dt.year == year:
                    filtered.append(r)
            return filtered
        except ValueError:
            print("Invalid year input.")
            return []

    # 4. Category
    elif choice == "4":
        categories = list({r["category"].strip() for r in receipts_list})
        print("\nSelect Category:")
        for idx, cat in enumerate(categories, start=1):
            print(f"{idx}. {cat}")

        sel = input("Option number: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(categories):
            selected_cat = categories[int(sel) - 1]
            return [
                r
                for r in receipts_list
                if r["category"].strip().lower() == selected_cat.lower()
            ]
        print("Invalid category selection.")
        return []

    # 5. Business
    elif choice == "5":
        businesses = list({r["business_name"].strip() for r in receipts_list})
        print("\nSelect Business:")
        for idx, biz in enumerate(businesses, start=1):
            print(f"{idx}. {biz}")

        sel = input("Option number: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(businesses):
            selected_biz = businesses[int(sel) - 1]
            return [
                r
                for r in receipts_list
                if r["business_name"].strip().lower() == selected_biz.lower()
            ]
        print("Invalid business selection.")
        return []

    else:
        print("Invalid option selected.")
        return []


def export_receipts_to_downloads(receipts_list: list[dict]) -> None:
    """Filters data and saves CSV or JSON files directly to the system Downloads folder."""
    filtered_data = filter_receipts_for_export(receipts_list)

    if not filtered_data:
        print("No matching receipts found to export.")
        return

    # Locates your operating system's default Downloads directory
    downloads_folder = os.path.expanduser("~/Downloads")

    # Safety check to ensure the folder exists
    os.makedirs(downloads_folder, exist_ok=True)

    print("\nSelect Export Format:")
    print("1. CSV")
    print("2. JSON")
    format_choice = input("Option (1-2): ").strip()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save as CSV
    if format_choice == "1":
        file_name = f"receipts_export_{timestamp}.csv"
        file_path = os.path.join(downloads_folder, file_name)

        fieldnames = [
            "id",
            "business_name",
            "date",
            "category",
            "amount",
            "vat",
            "payment_method",
            "created_at",
        ]

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file, fieldnames=fieldnames, extrasaction="ignore"
                )
                writer.writeheader()
                writer.writerows(filtered_data)

            print("\n" + "=" * 60)
            print("SUCCESS! File exported to your Downloads folder.")
            print(f"File Name: {file_name}")
            print(f"Full Path: {file_path}")
            print("=" * 60)

        except Exception as e:
            print(f"Failed to export file: {e}")

    # Save as JSON
    elif format_choice == "2":
        file_name = f"receipts_export_{timestamp}.json"
        file_path = os.path.join(downloads_folder, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(filtered_data, file, indent=4)

            print("\n" + "=" * 60)
            print("SUCCESS! File exported to your Downloads folder.")
            print(f"File Name: {file_name}")
            print(f"Full Path: {file_path}")
            print("=" * 60)

        except Exception as e:
            print(f"Failed to export file: {e}")

    else:
        print("Invalid format choice.")