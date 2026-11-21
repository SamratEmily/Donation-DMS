"""
Seed the database with demo data: areas, donors, volunteers, donations of
every type and status, collection requests and delivery gallery images.

Safe to run more than once - existing seed records are reused, not duplicated.

    python manage.py seed_data
"""
import io
from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from areas.models import DonationArea
from donations.models import Donation, DonationCollectionRequest
from donors.models import Donor
from gallery.models import Gallery
from volunteers.models import Volunteer

ADMIN = ("admin@example.com", "admin123")

AREAS = [
    ("Mirpur", "Mirpur 1-14 including Pallabi and Kazipara."),
    ("Uttara", "Uttara sectors 1-18 and Abdullahpur."),
    ("Dhanmondi", "Dhanmondi, Jigatola and Kalabagan."),
    ("Mohammadpur", "Mohammadpur, Adabor and Shyamoli."),
    ("Old Dhaka", "Lalbagh, Chawkbazar and Sadarghat."),
    ("Gazipur", "Tongi and Gazipur city (currently paused).", False),
]

# email, first, last, phone, address   (password for all: donor123)
DONORS = [
    ("donor@example.com", "Demo", "Donor", "01711000001", "House 12, Road 5, Dhanmondi"),
    ("rahim.donor@example.com", "Rahim", "Uddin", "01711000002", "Sector 7, Uttara"),
    ("nusrat.donor@example.com", "Nusrat", "Jahan", "01711000003", "Mirpur 10, Dhaka"),
    ("karim.donor@example.com", "Karim", "Ahmed", "01711000004", "Lalbagh, Old Dhaka"),
]

# email, first, last, phone, status, area   (password for all: volunteer123)
VOLUNTEERS = [
    ("volunteer@example.com", "Demo", "Volunteer", "01811000001", "ACCEPTED", "Mirpur"),
    ("tania.vol@example.com", "Tania", "Akter", "01811000002", "ACCEPTED", "Uttara"),
    ("sakib.vol@example.com", "Sakib", "Hasan", "01811000003", "ACCEPTED", "Dhanmondi"),
    ("mitu.vol@example.com", "Mitu", "Rahman", "01811000004", "ACCEPTED", "Old Dhaka"),
    ("pending.vol@example.com", "Arif", "Hossain", "01811000005", "PENDING", None),
    ("rejected.vol@example.com", "Jamal", "Sheikh", "01811000006", "REJECTED", None),
]

# donor email, type, quantity, description, area, status, days ago, admin remark
DONATIONS = [
    # NEW - waiting for admin review
    ("donor@example.com", "FOOD", "20 kg rice", "Rice and lentils for families in need.", "Mirpur", "NEW", 1, ""),
    ("donor@example.com", "BOOKS", "35 books", "Class 6-8 textbooks in good condition.", None, "NEW", 2, ""),
    ("rahim.donor@example.com", "MONEY", "5,000 BDT", "Cash for winter blankets.", "Uttara", "NEW", 0, ""),
    ("nusrat.donor@example.com", "TOYS", "15 items", "Soft toys and puzzles for children.", None, "NEW", 3, ""),
    # ACCEPTED - visible to the volunteer of that area
    ("donor@example.com", "CLOTHES", "3 bags", "Winter jackets and sweaters, washed and folded.", "Mirpur", "ACCEPTED", 5, "Accepted - please collect this week."),
    ("nusrat.donor@example.com", "MEDICINE", "2 boxes", "Paracetamol, ORS and bandages (not expired).", "Mirpur", "ACCEPTED", 4, "Check expiry dates on pickup."),
    ("karim.donor@example.com", "FOOD", "50 food packs", "Iftar packs: dates, puffed rice, juice.", "Mirpur", "ACCEPTED", 6, "Urgent - deliver before Friday."),
    ("rahim.donor@example.com", "BOOKS", "1 shelf", "Story books for the community library.", "Uttara", "ACCEPTED", 7, ""),
    ("karim.donor@example.com", "OTHER", "2 ceiling fans", "Working fans for the school classroom.", "Old Dhaka", "ACCEPTED", 8, ""),
    # COLLECTED - picked up by a volunteer, not yet delivered
    ("donor@example.com", "TOYS", "1 carton", "Board games and building blocks.", "Mirpur", "COLLECTED", 12, "Accepted."),
    ("rahim.donor@example.com", "CLOTHES", "40 pieces", "School uniforms, various sizes.", "Uttara", "COLLECTED", 14, "Accepted."),
    ("nusrat.donor@example.com", "MEDICINE", "1 first-aid kit", "Complete first-aid kit for the clinic.", "Dhanmondi", "COLLECTED", 10, "Accepted."),
    # DELIVERED - completed, with gallery photo
    ("donor@example.com", "FOOD", "100 kg rice", "Monthly rice support for 20 families.", "Mirpur", "DELIVERED", 30, "Delivered to 20 families."),
    ("donor@example.com", "MONEY", "10,000 BDT", "Funds used to buy school supplies.", "Dhanmondi", "DELIVERED", 40, "Converted to school supplies."),
    ("rahim.donor@example.com", "CLOTHES", "60 blankets", "Winter blankets for street children.", "Uttara", "DELIVERED", 25, "Delivered at the shelter."),
    ("karim.donor@example.com", "BOOKS", "80 books", "Library starter set for a local school.", "Old Dhaka", "DELIVERED", 45, "Handed over to the headteacher."),
    ("nusrat.donor@example.com", "TOYS", "30 toys", "Eid gifts for orphanage children.", "Mirpur", "DELIVERED", 20, "Delivered on Eid morning."),
    # REJECTED
    ("karim.donor@example.com", "MEDICINE", "Expired syrup bottles", "Cough syrup, expiry 2024.", None, "REJECTED", 9, "Rejected - medicines are expired."),
    ("rahim.donor@example.com", "OTHER", "Old TV", "CRT television, not working.", None, "REJECTED", 16, "Rejected - we cannot accept broken electronics."),
]

# (top-left, bottom-right) gradient colours per donation type
TYPE_COLORS = {
    "FOOD": ((251, 146, 60), (234, 88, 12)),
    "CLOTHES": ((96, 165, 250), (37, 99, 235)),
    "MONEY": ((74, 222, 128), (22, 163, 74)),
    "BOOKS": ((192, 132, 252), (124, 58, 237)),
    "TOYS": ((251, 113, 133), (225, 29, 72)),
    "MEDICINE": ((45, 212, 191), (13, 148, 136)),
    "OTHER": ((148, 163, 184), (71, 85, 105)),
}

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",   # macOS
    "C:/Windows/Fonts/arialbd.ttf",                         # Windows
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
    "DejaVuSans-Bold.ttf",
]


def _font(size):
    from PIL import ImageFont
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


def placeholder_image(donation):
    """Generate a gradient JPEG card to stand in for a delivery photo."""
    from PIL import Image, ImageDraw

    W, H = 1200, 750
    c1, c2 = TYPE_COLORS.get(donation.donation_type, TYPE_COLORS["OTHER"])
    # diagonal gradient
    base = Image.linear_gradient("L")  # 256x256, black (top) -> white (bottom)
    grad = Image.blend(base.resize((W, H)), base.rotate(90).transpose(Image.FLIP_LEFT_RIGHT).resize((W, H)), 0.5)
    img = Image.composite(Image.new("RGB", (W, H), c2), Image.new("RGB", (W, H), c1), grad)
    draw = ImageDraw.Draw(img, "RGBA")

    # soft decorative circles
    draw.ellipse((W - 420, -220, W + 180, 380), fill=(255, 255, 255, 38))
    draw.ellipse((-200, H - 260, 260, H + 200), fill=(255, 255, 255, 26))

    def centered(text, font, y, fill=(255, 255, 255, 255)):
        w = draw.textbbox((0, 0), text, font=font)[2]
        draw.text(((W - w) / 2, y), text, fill=fill, font=font)

    centered(donation.get_donation_type_display().upper(), _font(40), 205, (255, 255, 255, 210))
    centered(donation.quantity, _font(104), 270)

    pill = f"Delivered  ·  {donation.area.name}" if donation.area else "Delivered"
    pf = _font(36)
    pw = draw.textbbox((0, 0), pill, font=pf)[2]
    x0, y0 = (W - pw) / 2 - 34, 455
    draw.rounded_rectangle((x0, y0, x0 + pw + 68, y0 + 70), radius=35, fill=(255, 255, 255, 235))
    draw.text((x0 + 34, y0 + 15), pill, fill=c2, font=pf)

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return ContentFile(buf.getvalue(), name=f"seed_donation_{donation.pk}.jpg")


class Command(BaseCommand):
    help = "Load demo data (areas, donors, volunteers, donations, collections, gallery)."

    def user(self, email, password, role, first, last, **extra):
        u, created = User.objects.get_or_create(
            email=email, defaults={"role": role, "first_name": first, "last_name": last, **extra}
        )
        if created:
            u.set_password(password)
            u.save()
        return u

    @transaction.atomic
    def handle(self, *args, **options):
        now = timezone.now()

        admin = self.user(*ADMIN, "ADMIN", "Admin", "User", is_staff=True, is_superuser=True)

        areas = {}
        for name, desc, *active in AREAS:
            areas[name], _ = DonationArea.objects.get_or_create(
                name=name, defaults={"description": desc, "is_active": active[0] if active else True}
            )

        donors = {}
        for email, first, last, phone, address in DONORS:
            u = self.user(email, "donor123", "DONOR", first, last)
            donors[email], _ = Donor.objects.get_or_create(
                user=u, defaults={"phone": phone, "address": address}
            )

        volunteers = {}
        for email, first, last, phone, status, area in VOLUNTEERS:
            u = self.user(email, "volunteer123", "VOLUNTEER", first, last)
            v, created = Volunteer.objects.get_or_create(
                user=u, defaults={"phone": phone, "status": status, "assigned_area": areas.get(area)}
            )
            if not created and v.status == "ACCEPTED" and area and not v.assigned_area:
                v.assigned_area = areas[area]
                v.save()
            volunteers[email] = v
        vol_by_area = {v.assigned_area.name: v for v in volunteers.values()
                       if v.status == "ACCEPTED" and v.assigned_area}

        made = 0
        for i, (email, dtype, qty, desc, area, status, days, remark) in enumerate(DONATIONS):
            donation, created = Donation.objects.get_or_create(
                donor=donors[email], donation_type=dtype, quantity=qty,
                defaults={"description": desc, "area": areas.get(area),
                          "status": status, "admin_remark": remark},
            )
            if not created:
                continue
            made += 1
            when = now - timedelta(days=days, hours=i)
            Donation.objects.filter(pk=donation.pk).update(created_at=when, updated_at=when + timedelta(days=min(days, 2)))

            vol = vol_by_area.get(area)
            if vol and status == "ACCEPTED" and i % 2 == 0:
                DonationCollectionRequest.objects.create(
                    donation=donation, volunteer=vol, status="IN_PROGRESS",
                    notes="Contacted donor, pickup scheduled.")
            elif vol and status in ("COLLECTED", "DELIVERED"):
                DonationCollectionRequest.objects.create(
                    donation=donation, volunteer=vol, status="COMPLETED",
                    notes="Collected from donor's address.", collected_at=when + timedelta(days=1))

            if status == "DELIVERED":
                Gallery.objects.create(
                    donation=donation, image=placeholder_image(donation),
                    caption=f"{donation.get_donation_type_display()} delivered in {area}",
                    uploaded_by=vol.user if vol else admin)

        self.stdout.write(self.style.SUCCESS(
            f"Seed data ready: {len(areas)} areas, {len(donors)} donors, "
            f"{len(volunteers)} volunteers, {made} new donations "
            f"({Donation.objects.count()} donations in total)."))
        self.stdout.write("Logins: admin@example.com/admin123, donor@example.com/donor123, "
                          "volunteer@example.com/volunteer123")
