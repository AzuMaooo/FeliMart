from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Seeds the database with FeliMart starter products'

    def handle(self, *args, **kwargs):
        products = [
            {
                'name': 'Salmon',
                'description': 'Freeze-dried salmon flakes, rich in omega-3s for a shiny coat. A crunchy, protein-packed treat most cats find hard to resist.',
                'price': 5.90,
                'stock_quantity': 40,
                'category': 'food',
                'rarity': 'common',
            },
            {
                'name': 'Egg',
                'description': 'Steamed egg crumbles, a soft, protein-rich snack that is gentle on sensitive stomachs. A favorite for kittens and picky eaters alike.',
                'price': 4.50,
                'stock_quantity': 35,
                'category': 'food',
                'rarity': 'common',
            },
            {
                'name': 'Corn',
                'description': 'Sweet corn kernels, lightly roasted for a crunchy texture. A fun, fiber-rich snack that adds variety to mealtime.',
                'price': 3.90,
                'stock_quantity': 50,
                'category': 'food',
                'rarity': 'common',
            },
            {
                'name': 'Carrot',
                'description': 'Freeze-dried carrot chips, naturally sweet and crunchy. A low-calorie treat that is great for cats who enjoy a bit of veggie crunch.',
                'price': 3.50,
                'stock_quantity': 45,
                'category': 'food',
                'rarity': 'common',
            },
            {
                'name': 'Pumpkin',
                'description': 'Pureed pumpkin bites, soft and easy to digest. Known to support healthy digestion, a gentle everyday treat.',
                'price': 4.20,
                'stock_quantity': 30,
                'category': 'food',
                'rarity': 'common',
            },
            {
                'name': 'Gourmet Tuna Feast',
                'description': 'A limited-batch tuna dish made with wild-caught tuna and a touch of bonito broth. Expensive, hard to source, and adored by nearly every cat who tries it.',
                'price': 28.00,
                'stock_quantity': 6,
                'category': 'food',
                'rarity': 'rare',
            },
            {
                'name': 'Feather Wand Toy',
                'description': 'A springy wand with dangling feathers, perfect for triggering your cat\'s pounce instinct. Interactive play that keeps them engaged for hours.',
                'price': 9.90,
                'stock_quantity': 25,
                'category': 'toy',
                'rarity': 'common',
            },
            {
                'name': 'Crinkle Ball',
                'description': 'A lightweight ball that crinkles with every bat and roll. Simple, satisfying, and a solo-play favorite.',
                'price': 6.50,
                'stock_quantity': 30,
                'category': 'toy',
                'rarity': 'common',
            },
            {
                'name': 'Catnip Mouse',
                'description': 'A soft plush mouse stuffed with premium catnip. Irresistible for most cats, guaranteed to spark some chaotic zoomies.',
                'price': 7.90,
                'stock_quantity': 28,
                'category': 'toy',
                'rarity': 'common',
            },
            {
                'name': 'Cozy Knit Bed',
                'description': 'A soft, machine-washable knit bed sized for curling up. Warm, snug, and easy to keep clean.',
                'price': 32.00,
                'stock_quantity': 15,
                'category': 'accessory',
                'rarity': 'common',
            },
            {
                'name': 'Woven Cat Collar',
                'description': 'A breathable woven collar with a safety-release buckle. Comfortable for all-day wear.',
                'price': 12.50,
                'stock_quantity': 20,
                'category': 'accessory',
                'rarity': 'common',
            },
            {
                'name': 'Sunset Cat Perch Cushion',
                'description': 'A padded window perch cushion with a suction-mount frame, giving your cat a cozy front-row seat to birdwatch and soak up the sun.',
                'price': 24.90,
                'stock_quantity': 12,
                'category': 'accessory',
                'rarity': 'common',
            },
        ]

        for item in products:
            Product.objects.create(**item)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(products)} products successfully.'))
