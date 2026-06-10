from pathlib import Path
import logging

file_log_path = Path(__file__).parent / "arena_tickets.log"

logging.basicConfig(
    filename=file_log_path,
    level=logging.INFO,
    # với %(asctime)s là thời gian ghi log, %(levelname)s là mức độ của log, %(message)s là nội dung log
    format="%(asctime)s -  %(levelname)s - %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S"
)

ticket_db = [
    {"ticket_id": "T01", "buyer_name": "Nguyen Van A",
        "price": 500.0, "status": "Booked", "seat": ("A", 1)},

    {"ticket_id": "T02", "buyer_name": "Tran Thi B",
        "price": 300.0, "status": "Cancelled", "seat": ("B", 5)},

    {"ticket_id": "T03", "buyer_name": "Le Van C",
        "price": 500.0, "status": "Booked", "seat": ("A", 2)}
]


def find_ticket(tickets, id):
    for ticket in tickets:
        if ticket['ticket_id'] == id:
            return ticket
    return None


def display_tickets(tickets):
    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    print("\n--- DANH SÁCH VÉ ---")
    print(f"{'Mã Vé':<5} | {'Tên Khách Hàng':<19}  | {'Giá Vé':<9}  | {'Chỗ Ngồi':<10} | Trạng Thái")
    print("-"*79)

    try:
        for ticket in tickets:
            seat = f"{ticket['seat'][0]} - {ticket['seat'][1]}"
            status = ticket['status']

            if status == "Cancelled":
                status += " [ĐÃ HỦY]"

            print(
                f"{ticket['ticket_id']:<5} | "
                f"{ticket['buyer_name']:<20} | "
                f"{ticket['price']:<10} | "
                f"{seat:<10} | "
                f"{status}"
            )

        logging.info("User viewed ticket list.")

    except KeyError as error:
        print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
        logging.error(f"Missing key while displaying ticket: '{error}'")
    print("-"*79)


def book_ticket(tickets):
    print("\n--- ĐẶT VÉ MỚI ---")
    while True:
        booked_id = input("Nhập mã vé: ").strip().upper()

        if booked_id == "":
            print("Không được để trống")
            continue

        if find_ticket(tickets, booked_id):
            print(f"Lỗi: Mã vé {booked_id} đã tồn tại.")
            logging.warning(f"Duplicate ticket ID entered: {booked_id}")
            continue
        break

    while True:
        buyer_name = input("Nhập tên khách hàng: ").strip().title()

        if buyer_name == "":
            print("Không được để trống")
            continue
        break

    while True:
        try:
            price = float(input("Nhập giá vé: ").strip())

            if price <= 0:
                print("\nGiá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break

        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")

    while True:
        seat_row = input("Nhập khu vực ghế: ").strip().upper()

        if seat_row == "":
            print("Không được để trống")
            continue
        break

    while True:
        try:
            seat_number = int(input("Nhập số ghế: ").strip())
            break
        except ValueError:
            print("Số ghế phải là số nguyên.")

    tickets.append({
        "ticket_id": booked_id,
        "buyer_name": buyer_name,
        "price": price,
        "status": "Booked",
        "seat": (seat_row, seat_number)
    })

    print(f"\nThành công: Đã đặt vé {booked_id} cho khách hàng {buyer_name}.")
    logging.info(f"Booked new ticket {booked_id} for {buyer_name}")


def change_seat(tickets):
    print("\n--- ĐỔI CHỖ NGỒI ---")
    while True:
        change_id = input("Nhập mã vé cần đổi chỗ: ").strip().upper()

        if change_id == "":
            print("Không được để trống")
            continue
        break

    ticket = find_ticket(tickets, change_id)

    if ticket:
        while True:
            new_row = input("Nhập khu vực ghế: ").strip().upper()

            if new_row == "":
                print("Không được để trống")
                continue
            break

        while True:
            try:
                new_number = int(input("Nhập số ghế: ").strip())
                break
            except ValueError:
                print("Số ghế phải là số nguyên.")

        ticket['seat'] = (new_row, new_number)

        print(f"\nThành công: Đã đổi chỗ vé {change_id} sang {new_row}-{new_number}.")
        logging.info(f"Seat changed for ticket {change_id} to {new_row}-{new_number}")
    
    else:
        print(f"\nKhông tìm thấy vé mang mã {change_id}.")
        logging.warning(f"Change seat failed - Ticket {change_id} not found")


def cancel_ticket(tickets):
    print("\n--- HỦY VÉ ---")
    while True:
        cancel_id = input("Nhập mã vé cần đổi chỗ: ").strip().upper()

        if cancel_id == "":
            print("Không được để trống")
            continue
        break

    ticket = find_ticket(tickets, cancel_id)

    if ticket:
        if ticket['status'] == "Cancelled":
            print(f"\nVé {cancel_id} đã ở trạng thái Cancelled trước đó.")
        else:
            ticket['status'] = "Cancelled"
            print(f"\nThành công: Vé {cancel_id} đã được hủy.")
            logging.warning(f"Ticket {cancel_id} has been cancelled.")
    else:
        print(f"\nKhông tìm thấy vé mang mã {cancel_id}.")
        logging.warning(f"Change seat failed - Ticket {cancel_id} not found")


def calculate_total_revenue(ticket_list)->float:
    total = 0
    for ticket in ticket_list:
        if ticket["status"] == "Booked":
            total += ticket["price"]
    return total


def calculate_revenue(tickets):
    booked_count = 0
    cancelled_count = 0

    try:
        for ticket in tickets:
            if ticket['status'] == "Booked":
                booked_count += 1
            else:
                cancelled_count += 1

        total = calculate_total_revenue(tickets)
        print(f"Tổng số vé đã đặt: {booked_count}")
        print(f"Tổng số vé đã hủy: {cancelled_count}")
        print(f"Tổng doanh thu hợp lệ: {total:,}")
        logging.info(f"Revenue report generated. Total: {total}")

    except KeyError as error:
        print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
        print("Tổng doanh thu hợp lệ: 0.0")
        logging.error(f"Missing key while calculating revenue: {error}")


def main():
    while True:
        choice = input('''
=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===
1. Xem danh sách vé đã bán
2. Đặt vé mới
3. Đổi chỗ ngồi (Cập nhật vé)
4. Hủy vé
5. Báo cáo doanh thu
6. Thoát chương trình
======================================== 
"Chọn chức năng (1-6): ''').strip()
    
        match choice:
            case "1":
                display_tickets(ticket_db)

            case "2":
                book_ticket(ticket_db)

            case "3":
                change_seat(ticket_db)

            case "4":
                cancel_ticket(ticket_db)

            case "5":
                calculate_revenue(ticket_db)

            case "6":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
                logging.info("Ticket management system closed.")
                break
            case _:
                print("Lựa chọn không hợp lệ, vui lòng nhập 1-6")


if __name__ == "__main__":
    main()