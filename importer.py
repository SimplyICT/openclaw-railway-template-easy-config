import os
from supabase import create_client

def insert_data():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        return "Missing Supabase credentials"

    supabase = create_client(url, key)

    data = [
        {"site": "Benowa ELC", "type": "Desktop", "brand": "HP Prodesk 500 G4 SFF", "serial": "2VG42AV", "user": "BELC-Admin-Main", "ignore": True},
        {"site": "Benowa ELC", "type": "Desktop", "brand": "Generic I5", "serial": "BELC-Admin-Second", "user": "BELC-Admin-Second", "ignore": True},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Hp 15S-fq3xxx", "serial": "4Z207PA#ABG", "user": "Babies One", "win_up": "yes", "sec_check": "yes", "os": "win 11 home"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Acer Aspire AL15-51M", "serial": "NXKS5SA003343022C10X15", "user": "Babies Two", "win_up": "yes", "sec_check": "yes", "os": "win 11 home"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Inspiron 16 5640", "serial": "C428GB4", "user": "Kate", "os": "missing"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Dell 15 DC1520", "serial": "9DVJ4C4", "user": "Kindy One", "purchase_date": "2025-08-28", "win_up": "yes", "sec_check": "yes", "os": "win 11 pro"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Dell 15 DC1520", "serial": "hbvDPC4", "user": "Kindy Two", "purchase_date": "2025-08-28", "os": "missing"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Dell Inspiron 16 7640 2 in 1", "serial": "CMTF044", "user": "Kylie", "purchase_date": "2024-08-16", "os": "missing"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "HP 15s-eq2xxx", "serial": "5CD2170QH1Y", "user": "Melissa", "win_up": "yes", "sec_check": "yes", "os": "win 11 pro"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "HP 15S-fq3xxx", "serial": "4z2007pa#ABG", "user": "OSHC", "os": "missing"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "HP 15-FD0xxx", "serial": "B69K9PA#ABG", "user": "Pre Kindy", "os": "missing"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "HP 15-FD0xxx", "serial": "B69K9PA#ABG_2", "user": "Senior Kindy", "win_up": "yes", "sec_check": "yes", "os": "win 11 home"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Dell Inspiron 16 7640 2 in 1", "serial": "JHWW444", "user": "Simona", "purchase_date": "2024-08-16", "os": "missing"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Acer Aspire AL15-51M", "serial": "NXXRSSA00134300fb50x15", "user": "Toddlers One", "os": "missing"},
        {"site": "Benowa ELC", "type": "Laptop", "brand": "Dell Inspiron 14 5440", "serial": "1NWK494", "user": "Toddlers Two", "win_up": "yes", "sec_check": "yes", "os": "win 11 pro"}
    ]

    for row in data:
        # Upsert device
        supabase.table("devices").upsert({
            "serial_number": row["serial"],
            "device_type": row["type"],
            "brand_model": row["brand"],
            "date_of_purchase": row.get("purchase_date"),
            "assigned_user_room": row["user"]
        }).execute()

        # Insert audit entry
        supabase.table("audit_entries").insert({
            "serial_number": row["serial"],
            "site_name": row["site"],
            "windows_os": row.get("os"),
            "windows_updates": row.get("win_up"),
            "security_check": row.get("sec_check"),
            "ignore_flag": row.get("ignore", False)
        }).execute()

    return "Data processing complete"

if __name__ == "__main__":
    print(insert_data())
