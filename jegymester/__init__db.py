﻿from __future__ import annotations
from datetime import datetime

from app import db, create_app
from config import Config
from app.models.user import User
from app.models.role import Role
from app.models.userrole import UserRole
from app.models.movie import Movie
from app.models.theater import Theater
from app.models.seat import Seat
from app.models.screening import Screening
from app.models.ticketcategory import TicketCategory
from app.models.order import Order, StatusEnum
from app.models.ticket import Ticket
from app.models.ticketorder import TicketOrder

# Create the Flask app and push the app context
app = create_app(config_class=Config)
app.app_context().push()

# Verify database configuration
if not app.config.get("SQLALCHEMY_DATABASE_URI"):
    raise ValueError("Database URI not set in configuration")

try:
    # Drop and recreate tables (optional, comment out if not desired)
   # db.drop_all()
   # db.create_all()

    # Roles
    if not Role.query.filter_by(rolename="Admin").first():
        db.session.add_all([
            Role(rolename="Admin"),
            Role(rolename="User"),
            Role(rolename="Cashier"),
            Role(rolename="Guest")
        ])
        db.session.commit()

    # Test User
    if not User.query.filter_by(email="testuser@example.com").first():
        user = User(email="testuser@example.com", phone="+36123456789")
        # Assumes set_password hashes the password
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Assign roles to user
    user = User.query.filter_by(email="testuser@example.com").first()
    admin_role = Role.query.filter_by(rolename="Admin").first()
    user_role = Role.query.filter_by(rolename="User").first()
    if admin_role not in user.roles:
        user.roles.append(admin_role)
    if user_role not in user.roles:
        user.roles.append(user_role)
    db.session.commit()

    # Movies
    if not Movie.query.filter_by(title="Titanic").first():
        movie = Movie(
            title="Titanic",
            duration=194,
            genre="Drama",
            age_limit=12,
            description="A love story on a sinking ship"
        )
        db.session.add(movie)
    if not Movie.query.filter_by(title="Mátrix").first():
        movie2 = Movie(
            title="Mátrix",
            duration=136,
            genre="Sci-Fi",
            age_limit=16,
            description="Reality is a simulation"
        )
        db.session.add(movie2)
    if not Movie.query.filter_by(title="Zalán_futása").first():
        movie3 = Movie(
            title="Zalán_futása",
            duration=200,
            genre="Adventure",
            age_limit=18,
            description="Run away as fast as you can from Zalan"
        )
        db.session.add(movie3)
    if not Movie.query.filter_by(title="Egyetemistak_elete").first():
        movie4 = Movie(
            title="Egyetemistak_elete",
            duration=90,
            genre="Reality",
            age_limit=16,
            description="Look behind the curtian, what happening in an uni"
        )
        db.session.add(movie4)
    if not Movie.query.filter_by(title="A_nagy_kanape_pakolas").first():
        movie5 = Movie(
            title="A_nagy_kanape_pakolas",
            duration=60,
            genre="Documentary",
            age_limit=10,
            description="Come with us, and we show you how you sucessfully outbring a sofa from a tiny apartmen"
        )
        db.session.add(movie5)
    if not Movie.query.filter_by(title="ETS_GRIND").first():
        movie6 = Movie(
            title="ETS_GRIND",
            duration=60,
            genre="Funny",
            age_limit=10,
            description="Come to a beautiful trip to the simulators world"
        )
        db.session.add(movie6)
    db.session.commit()

    # Theaters
    if not Theater.query.filter_by(theatname="Főterem").first():
        theater = Theater(theatname="Főterem")
        db.session.add(theater)
    if not Theater.query.filter_by(theatname="Kisterem").first():
        theater2 = Theater(theatname="Kisterem")
        db.session.add(theater2)
    db.session.commit()

    # Seats
    theater1 = Theater.query.filter_by(theatname="Főterem").first()
    theater2 = Theater.query.filter_by(theatname="Kisterem").first()
    if not Seat.query.filter_by(theater_id=theater1.id, seat_number="A1").first():
        db.session.add_all([
            Seat(theater_id=theater1.id, seat_number=f"{row}{i}")
            for row in ["A", "B", "C"]
            for i in range(1, 2)
        ] + [
            Seat(theater_id=theater2.id, seat_number=f"{row}{i}")
            for row in ["A", "B", "C"]
            for i in range(1, 2)
        ])
        db.session.commit()

    # Screenings
    movie1 = Movie.query.filter_by(title="Titanic").first()
    movie2 = Movie.query.filter_by(title="Mátrix").first()
    if not Screening.query.filter_by(movie_id=movie1.id, theater_id=theater1.id).first():
        screening = Screening(
            movie_id=movie1.id,
            theater_id=theater1.id,
            start_time=datetime(2025, 3, 10, 18, 0)
        )
        screening2 = Screening(
            movie_id=movie2.id,
            theater_id=theater2.id,
            start_time=datetime(2025, 3, 10, 20, 0)
        )
        db.session.add_all([screening, screening2])
        db.session.commit()

    # Ticket Categories
    if not TicketCategory.query.filter_by(catname="Felnőtt").first():
        db.session.add_all([
            TicketCategory(catname="Felnőtt", price=2500),
            TicketCategory(catname="Diák", price=2000),
            TicketCategory(catname="Nyugdíjas", price=1800)
        ])
        db.session.commit()

    # Orders
    if not Order.query.filter_by(payment_status=StatusEnum.Successful).first():
        order = Order(payment_status=StatusEnum.Successful)
        db.session.add(order)
        db.session.commit()

    # Tickets
    screening1 = Screening.query.filter_by(movie_id=movie1.id).first()
    screening2 = Screening.query.filter_by(movie_id=movie2.id).first()
    adult_category = TicketCategory.query.filter_by(catname="Felnőtt").first()
    student_category = TicketCategory.query.filter_by(catname="Diák").first()
    seat1 = Seat.query.filter_by(
        theater_id=screening1.theater_id, reserved=False).first()
    seat2 = Seat.query.filter_by(
        theater_id=screening2.theater_id, reserved=False).first()
    if seat1 and seat2:
        if not Ticket.query.filter_by(screening_id=screening1.id, user_id=user.id).first():
            ticket = Ticket(screening_id=screening1.id, user_id=user.id,
                            ticketcategory_id=adult_category.id, seat_id=seat1.id)
            ticket2 = Ticket(screening_id=screening2.id, user_id=user.id,
                             ticketcategory_id=student_category.id, seat_id=seat2.id)
            db.session.add_all([ticket, ticket2])
            seat1.reserved = True
            seat2.reserved = True
            db.session.commit()

    # TicketOrder (junction table)
    order = Order.query.filter_by(payment_status=StatusEnum.Successful).first()
    ticket1 = Ticket.query.filter_by(screening_id=screening1.id).first()
    ticket2 = Ticket.query.filter_by(screening_id=screening2.id).first()
    if not TicketOrder.query.filter_by(ticket_id=ticket1.id).first():
        order.tickets.append(TicketOrder(
            ticket_id=ticket1.id, ticket_active=1))
        order.tickets.append(TicketOrder(
            ticket_id=ticket2.id, ticket_active=1))
        db.session.commit()

    # Example queries to verify data
    movie = Movie.query.first()
    print(f"Movie: {movie.title}, Duration: {movie.duration}")

    theater = Theater.query.first()
    print(f"Theater: {theater.theatname}")
    for seat in theater.seats:
        print(f"Seat: {seat.seat_number}")

    screening = Screening.query.first()
    print(f"Screening: {screening.movie.title} at {screening.start_time}")

    ticket = Ticket.query.first()
    print(
        f"Ticket for: {ticket.screening.movie.title}, Category: {ticket.ticketcategory.catname}")

except Exception as e:
    db.session.rollback()
    print(f"Error occurred: {e}")
    raise