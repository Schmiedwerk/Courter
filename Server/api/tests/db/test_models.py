import pytest
from sqlalchemy import select, text

from datetime import time, datetime, timedelta

from api.db.access import get_session
from api.db.models import create_tables, Admin, Employee, Customer, Timeslot, Court, Booking, Closing


TODAY = datetime.now().date()


@pytest.fixture(autouse=True)
async def setup_tables(setup_db):
    await create_tables()


@pytest.fixture
async def session(setup_db):
    async for session in get_session():
        await session.execute(text('pragma foreign_keys=on'))
        yield session


@pytest.fixture
async def populate_admins(session):
    admins = (
        Admin('admin1', 'fake_hash1'),
        Admin('admin2', 'fake_hash2'),
    )

    session.add_all(admins)
    await session.commit()

    return admins


@pytest.fixture
async def populate_employees(session):
    employees = (
        Employee('employee1', 'fake_hash1'),
        Employee('employee2', 'fake_hash2'),
        Employee('employee3', 'fake_hash3')
    )

    session.add_all(employees)
    await session.commit()

    return employees


@pytest.fixture
async def populate_customers(session):
    customers = (
        Customer('customer1', 'fake_hash1'),
        Customer('customer2', 'fake_hash2'),
        Customer('customer3', 'fake_hash3'),
        Customer('customer4', 'fake_hash4'),
        Customer('customer5', 'fake_hash5')
    )

    session.add_all(customers)
    await session.commit()

    return customers


@pytest.fixture
async def populate_timeslots(session):
    timeslots = (
        Timeslot(time(8), time(9)),
        Timeslot(time(9), time(10)),
        Timeslot(time(10), time(11)),
        Timeslot(time(12), time(13)),
        Timeslot(time(13), time(14)),
        Timeslot(time(15), time(16)),
        Timeslot(time(17), time(18))
    )

    session.add_all(timeslots)
    await session.commit()

    return timeslots


@pytest.fixture
async def populate_courts(session):
    courts = (
        Court('Wimbledon Centre Court', 'grass'),
        Court('Sydney SuperDome', 'hard'),
        Court('Rod Laver Arena', 'hard'),
        Court('Am Rothenbaum', 'clay'),
        Court('Novak Tennis Center', 'clay'),
        Court('Grandstand')
    )

    session.add_all(courts)
    await session.commit()

    return courts


@pytest.fixture
async def populate_bookings(session, populate_customers, populate_courts, populate_timeslots):
    bookings = (
        Booking(date=TODAY, timeslot_id=1, court_id=1, guest_name=None, customer_id=1),
        Booking(date=TODAY, timeslot_id=2, court_id=3, guest_name=None, customer_id=2),
        Booking(date=TODAY, timeslot_id=1, court_id=2, guest_name=None, customer_id=3),
        Booking(date=TODAY + timedelta(days=1), timeslot_id=1, court_id=2, guest_name=None, customer_id=3),
        Booking(date=TODAY + timedelta(days=2), timeslot_id=6, court_id=5, guest_name=None, customer_id=5),
        Booking(date=TODAY, timeslot_id=1, court_id=4, guest_name='Rafael Nadal', customer_id=None),
        Booking(date=TODAY, timeslot_id=7, court_id=6, guest_name='Steffi Graf', customer_id=None)
    )

    session.add_all(bookings)
    await session.commit()

    return bookings


@pytest.fixture
async def populate_closings(session, populate_courts, populate_timeslots):
    closings = (
        Closing(date=TODAY, start_timeslot_id=1, end_timeslot_id=7, court_id=6),
        Closing(date=TODAY + timedelta(days=7), start_timeslot_id=2, end_timeslot_id=4, court_id=2),
        Closing(date=TODAY + timedelta(days=13), start_timeslot_id=5, end_timeslot_id=5, court_id=5)
    )

    session.add_all(closings)
    await session.commit()

    return closings


async def test_save(session):
    customer = Customer('customer', 'fake_hash')
    await customer.save(session)
    session.expunge(customer)
    customer_db = await session.get(Customer, 1)
    assert customer_db == customer


async def test_delete(session, populate_employees):
    await populate_employees[2].delete(session)
    employees = await session.scalars(select(Employee))
    assert tuple(employees) == populate_employees[:2]


async def test_get_admin_by_existing_id(session, populate_admins):
    admin = await Admin.get(session, 1)
    assert admin == populate_admins[0]


async def test_get_admin_by_non_existing_id(session, populate_admins):
    admin = await Admin.get(session, 42)
    assert admin is None


async def test_get_admin_by_existing_name(session, populate_admins):
    admin = await Admin.get(session, 'admin1')
    assert admin == populate_admins[0]


async def test_get_admin_by_non_existing_name(session, populate_admins):
    admin = await Admin.get(session, 'root')
    assert admin is None


async def test_get_all_admins(session, populate_admins):
    admins = await Admin.get_all(session)
    assert tuple(admins) == populate_admins


async def test_get_employee_by_existing_id(session, populate_employees):
    employee = await Employee.get(session, 2)
    assert employee == populate_employees[1]


async def test_get_employee_by_non_existing_id(session, populate_employees):
    employee = await Employee.get(session, 57)
    assert employee is None


async def test_get_employee_by_existing_name(session, populate_employees):
    employee = await Employee.get(session, 'employee3')
    assert employee == populate_employees[2]


async def test_get_employee_by_non_existing_name(session, populate_employees):
    employee = await Employee.get(session, 'root')
    assert employee is None


async def test_get_all_employees(session, populate_employees):
    employees = await Employee.get_all(session)
    assert tuple(employees) == populate_employees


async def test_get_customer_by_existing_id(session, populate_customers):
    customer = await Customer.get(session, 4)
    assert customer == populate_customers[3]


async def test_get_customer_by_non_existing_id(session, populate_customers):
    customer = await Customer.get(session, 13)
    assert customer is None


async def test_get_customer_by_existing_name(session, populate_customers):
    customer = await Customer.get(session, 'customer5')
    assert customer == populate_customers[4]


async def test_get_customer_by_non_existing_name(session, populate_customers):
    customer = await Customer.get(session, 'customer42')
    assert customer is None


async def test_get_all_customers(session, populate_customers):
    customers = await Customer.get_all(session)
    assert tuple(customers) == populate_customers


async def test_get_customer_by_id_with_bookings(session, populate_customers, populate_bookings):
    customer = await Customer.get(session, 3, load_bookings=True)
    assert (customer == populate_customers[2] and
            customer.bookings == [populate_bookings[2], populate_bookings[3]])


async def test_customer_delete_cascade(session, populate_customers, populate_bookings):
    customer = await Customer.get(session, 3)
    await session.delete(customer)
    corresponding_bookings = await Booking.get_filtered(session, customer_id=3)
    assert len(tuple(corresponding_bookings)) == 0


async def test_get_timeslot_by_existing_id(session, populate_timeslots):
    timeslot = await Timeslot.get(session, 4)
    assert timeslot == populate_timeslots[3]


async def test_get_timeslot_by_non_existing_id(session, populate_timeslots):
    timeslot = await Timeslot.get(session, 25)
    assert timeslot is None


async def test_get_all_timeslots(session, populate_timeslots):
    timeslots = await Timeslot.get_all(session)
    assert tuple(timeslots) == populate_timeslots


async def test_get_court_by_existing_id(session, populate_courts):
    court = await Court.get(session, 4)
    assert court == populate_courts[3]


async def test_get_court_by_non_existing_id(session, populate_courts):
    court = await Court.get(session, 19)
    assert court is None


async def test_get_court_by_existing_name(session, populate_courts):
    court = await Court.get(session, 'Novak Tennis Center')
    assert court == populate_courts[-2]


async def test_get_court_by_non_existing_name(session, populate_courts):
    court = await Court.get(session, 'Lotus Court')
    assert court is None


async def test_get_all_courts(session, populate_courts):
    courts = await Court.get_all(session)
    assert tuple(courts) == populate_courts


async def test_get_customer_booking_by_existing_id(
        session, populate_bookings, populate_customers, populate_courts, populate_timeslots):
    booking = await Booking.get(session, 4)
    assert booking == populate_bookings[3]
    # test relationship configurations
    assert booking.customer == populate_customers[2]
    assert booking.timeslot == populate_timeslots[0]
    assert booking.court == populate_courts[1]


async def test_get_guest_booking_by_existing_id(session, populate_bookings, populate_courts, populate_timeslots):
    booking = await Booking.get(session, 6)
    assert booking == populate_bookings[5]
    # test relationship configurations
    assert booking.customer is None
    assert booking.timeslot == populate_timeslots[0]
    assert booking.court == populate_courts[3]


async def test_get_booking_by_non_existing_id(session, populate_bookings):
    booking = await Booking.get(session, 19)
    assert booking is None


async def test_get_all_bookings(session, populate_bookings):
    bookings = await Booking.get_all(session)
    assert tuple(bookings) == populate_bookings


async def test_get_bookings_by_existing_date(session, populate_bookings):
    bookings = await Booking.get_filtered(session, date=TODAY)
    assert tuple(bookings) == tuple(booking for booking in populate_bookings if booking.id not in (4, 5))


async def test_get_bookings_by_non_existing_date(session, populate_bookings):
    bookings = await Booking.get_filtered(session, date=TODAY + timedelta(days=7))
    assert len(tuple(bookings)) == 0


async def test_get_closing_by_existing_id(session, populate_closings, populate_courts, populate_timeslots):
    closing = await Closing.get(session, 2)
    assert closing == populate_closings[1]
    # test relationship configurations
    assert closing.court == populate_courts[1]
    assert closing.start_timeslot == populate_timeslots[1]
    assert closing.end_timeslot == populate_timeslots[3]
