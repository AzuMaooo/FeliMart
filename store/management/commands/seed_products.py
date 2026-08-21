from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Seeds the database with FeliMart starter products'

    def handle(self, *args, **kwargs):
        products = [
    {
        'name': 'Salmon',
        'description': 'Freeze-dried salmon, rich in omega-3s for a shiny coat. A crunchy, protein-packed treat and loved by most.',
        'price': 5.90,
        'stock_quantity': 40,
        'category': 'food',
        'rarity': 'common',
        'image': 'products/salmon.png',
    },
    {
        'name': 'Egg',
        'description': 'Soft, protein-rich snack that is gentle on sensitive stomachs. A favorite for picky eaters.',
        'price': 3.50,
        'stock_quantity': 35,
        'category': 'food',
        'rarity': 'common',
        'image': 'products/egg.png',
    },
    {
        'name': 'Corn',
        'description': 'Sweet corn, lightly roasted for a crunchy texture. Fiber-rich snack that adds variety to mealtime.',
        'price': 3.90,
        'stock_quantity': 50,
        'category': 'food',
        'rarity': 'common',
        'image': 'products/corn.png',
    },
    {
        'name': 'Carrot',
        'description': 'Freeze-dried carrots, naturally sweet and crunchy. A low-calorie treat.',
        'price': 3.50,
        'stock_quantity': 45,
        'category': 'food',
        'rarity': 'common',
        'image': 'products/carrot.png',
    },
    {
        'name': 'Pumpkin',
        'description': 'Pureed pumpkin bites, soft and easy to digest. Known to support healthy digestion, a gentle everyday treat.',
        'price': 4.20,
        'stock_quantity': 30,
        'category': 'food',
        'rarity': 'common',
        'image': 'products/pumpkin.png',
    },
    {
        'name': 'Gourmet Tuna Feast',
        'description': 'An exquisite limited edition tuna dish made with wild-caught tuna and a touch of bonito broth. Loved by all.',
        'price': 28.00,
        'stock_quantity': 6,
        'category': 'food',
        'rarity': 'rare',
        'image': 'products/gourmet_tuna_feast.png',
    },
    {
        'name': 'Feathery Wand Toy',
        'description': 'A springy wand with dangling feathers, fun for pouncing and pawing.',
        'price': 9.90,
        'stock_quantity': 25,
        'category': 'toy',
        'rarity': 'common',
        'image': 'products/feathery_wand_toy.png',
    },
    {
        'name': 'Squishy Slime Ball',
        'description': 'A stretchy, squishy ball that bounces back into shape after every bat and paw. Also a good friend to have around.',
        'price': 7.70,
        'stock_quantity': 30,
        'category': 'toy',
        'rarity': 'common',
        'image': 'products/squishy_slime_ball.png',
    },
    {
        'name': 'Catnip Mouse',
        'description': 'A soft plush mouse stuffed with catnip. Irresistibly guaranteed to spark some chaotic zoomies.',
        'price': 8.90,
        'stock_quantity': 28,
        'category': 'toy',
        'rarity': 'common',
        'image': 'products/catnip_mouse.png',
    },
    {
        'name': 'Cat Tree/Scratching Post',
        'description': 'A multi-level climbing, scratching, and napping post with a treasure to play on top.',
        'price': 32.00,
        'stock_quantity': 15,
        'category': 'accessory',
        'rarity': 'common',
        'image': 'products/cat_tree.png',
    },
    {
        'name': 'Bonita Ribbon',
        'description': 'Cutesy accessory that instantly makes the wearer more confident, and gives a fresh new look.',
        'price': 12.50,
        'stock_quantity': 20,
        'category': 'accessory',
        'rarity': 'common',
        'image': 'products/bonita_ribbon.png',
    },
    {
        'name': 'Homey Box',
        'description': 'Sturdy, perfect hiding or napping spot, irresistible pounce zone, no assembly required',
        'price': 19.90,
        'stock_quantity': 17,
        'category': 'accessory',
        'rarity': 'common',
        'image': 'products/homey_box.png',
    },
]

        for item in products:
            Product.objects.create(**item)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(products)} products successfully.'))
