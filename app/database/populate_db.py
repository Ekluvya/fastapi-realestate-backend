import asyncio
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from beanie import Document, init_beanie, Indexed
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Annotated
from enum import Enum
import random
# Property listing data converted from JavaScript to Python
list_data = [
    {
        "id": 1,
        "title": "Sea-Facing Apartment in Juhu Beach",
        "img": "https://images.pexels.com/photos/1918291/pexels-photo-1918291.jpeg",
        "bedroom": 2,
        "bathroom": 1,
        "price": 55000,
        "address": "Juhu Tara Road, Mumbai",
        "latitude": 19.1076,
        "longitude": 72.8266,
    },
    {
        "id": 2,
        "title": "Modern Studio in Connaught Place",
        "img": "https://images.pexels.com/photos/439391/pexels-photo-439391.jpeg",
        "bedroom": 1,
        "bathroom": 1,
        "price": 40000,
        "address": "Connaught Place, New Delhi",
        "latitude": 28.6315,
        "longitude": 77.2167,
    },
    {
        "id": 3,
        "title": "Cozy Cottage Near Ooty Lake",
        "img": "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
        "bedroom": 3,
        "bathroom": 2,
        "price": 30000,
        "address": "West Lake Road, Ooty",
        "latitude": 11.4064,
        "longitude": 76.6932,
    },
    {
        "id": 4,
        "title": "Luxury Villa with Private Pool in Goa",
        "img": "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",
        "bedroom": 5,
        "bathroom": 4,
        "price": 150000,
        "address": "Candolim Beach Road, Goa",
        "latitude": 15.5272,
        "longitude": 73.762,
    },
    {
        "id": 5,
        "title": "Affordable Apartment in Whitefield",
        "img": "https://images.pexels.com/photos/1643383/pexels-photo-1643383.jpeg",
        "bedroom": 2,
        "bathroom": 1,
        "price": 25000,
        "address": "Whitefield Main Road, Bangalore",
        "latitude": 12.9698,
        "longitude": 77.7499,
    },
    {
        "id": 6,
        "title": "Spacious Family Home in Anna Nagar",
        "img": "https://images.pexels.com/photos/1396132/pexels-photo-1396132.jpeg",
        "bedroom": 4,
        "bathroom": 2,
        "price": 60000,
        "address": "Anna Nagar West, Chennai",
        "latitude": 13.0906,
        "longitude": 80.2104,
    },
    {
        "id": 7,
        "title": "Chic Loft in Banjara Hills",
        "img": "https://images.pexels.com/photos/439391/pexels-photo-439391.jpeg",
        "bedroom": 2,
        "bathroom": 2,
        "price": 50000,
        "address": "Road No. 10, Banjara Hills, Hyderabad",
        "latitude": 17.412,
        "longitude": 78.4483,
    },
    {
        "id": 8,
        "title": "Penthouse with Rooftop in Koregaon Park",
        "img": "https://images.pexels.com/photos/323775/pexels-photo-323775.jpeg",
        "bedroom": 3,
        "bathroom": 3,
        "price": 120000,
        "address": "Koregaon Park, Pune",
        "latitude": 18.5362,
        "longitude": 73.9007,
    },
    {
        "id": 9,
        "title": "Rustic House Near Nainital Lake",
        "img": "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
        "bedroom": 4,
        "bathroom": 3,
        "price": 35000,
        "address": "Mallital, Nainital",
        "latitude": 29.3805,
        "longitude": 79.463,
    },
    {
        "id": 10,
        "title": "Minimalist Flat in South Extension",
        "img": "https://images.pexels.com/photos/1457842/pexels-photo-1457842.jpeg",
        "bedroom": 1,
        "bathroom": 1,
        "price": 38000,
        "address": "South Extension Part II, Delhi",
        "latitude": 28.5672,
        "longitude": 77.223,
    },
    {
        "id": 11,
        "title": "Stylish Condo Near Howrah Bridge",
        "img": "https://images.pexels.com/photos/439227/pexels-photo-439227.jpeg",
        "bedroom": 2,
        "bathroom": 2,
        "price": 42000,
        "address": "Howrah Bridge Road, Kolkata",
        "latitude": 22.585,
        "longitude": 88.3467,
    },
]

image_links = [
    "https://images.pexels.com/photos/439227/pexels-photo-439227.jpeg",
    "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
    "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg",
    "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
    "https://images.pexels.com/photos/271743/pexels-photo-271743.jpeg",
    "https://images.pexels.com/photos/37347/office-sitting-room-executive-sitting.jpg",
    "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",
    "https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg",
    "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
    "https://images.pexels.com/photos/276724/pexels-photo-276724.jpeg",
    "https://images.pexels.com/photos/271643/pexels-photo-271643.jpeg",
    "https://images.pexels.com/photos/323705/pexels-photo-323705.jpeg",
    "https://images.pexels.com/photos/271639/pexels-photo-271639.jpeg",
    "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg",
    "https://images.pexels.com/photos/37347/office-sitting-room-executive-sitting.jpg",
    "https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg",
    "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
    "https://images.pexels.com/photos/271743/pexels-photo-271743.jpeg",
    "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
    "https://images.pexels.com/photos/276724/pexels-photo-276724.jpeg",
    "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
    "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg",
    "https://images.pexels.com/photos/37347/office-sitting-room-executive-sitting.jpg",
    "https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg",
    "https://images.pexels.com/photos/37347/office-sitting-room-executive-sitting.jpg",
    "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",
    "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
    "https://images.pexels.com/photos/2102587/pexels-photo-2102587.jpeg",
    "https://images.pexels.com/photos/276724/pexels-photo-276724.jpeg",
    "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
    "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
    "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
    "https://images.pexels.com/photos/323705/pexels-photo-323705.jpeg",
    "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
    "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
    "https://images.pexels.com/photos/323705/pexels-photo-323705.jpeg",
    "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
    "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg",
    "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg",
    "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg"
]

class PropertyType(str, Enum):
    apartment = 'apartment'
    house = 'house'
    condo = 'condo'
    land = 'land'

class ContractType(str, Enum):
    buy = 'buy'
    rent = 'rent'

class PostDetail(BaseModel):
    id: UUID= Field(default_factory=uuid4)
    desc:str = Field(...)
    images:List[str] = Field(default_factory=list)
    utilities: Optional[str] = Field(...)
    pet: Optional[str] = Field(...)
    income: Optional[str] = Field(...)
    size: Optional[int] = Field(...)
    school: Optional[int] = Field(...)
    bus: Optional[int] = Field(...)
    restaurant: Optional[int] = Field(...)
    
class Post(Document):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(...)
    price: int = Field(...)
    img: str = Field(default_factory=str)
    address: str = Field(...)
    city: Annotated[str, Indexed()] = Field(...)
    bedroom: int = Field(...)
    bathroom: int = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
    p_type: PropertyType = Field(...)
    c_type: ContractType = Field(...)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None
    postDetail: PostDetail

    class Settings:
        name = "posts"
        use_revision = True  # Enable document revision tracking

# List of user IDs to assign to properties
user_ids = [
    UUID("a231de30-9072-4e3d-9304-9d7f8d331742"),
    UUID("dd543e31-e119-4c13-b33b-2ce52f9c7b18"),
    UUID("7793a397-49a8-4955-a737-a121af276790")
]


# Generate creative income requirement sentences
# Generate creative income requirement sentences
def generate_income_requirement(price: int) -> str:
    """Generate a humorous income requirement sentence based on property price."""
    import random
    
    # Base sentences that will be formatted with values
    base_phrases = [
        "You must be a {worth} to afford this!",
        "Annual income requirement: {income}",
        "Financial prerequisite: {worth}",
        "Only {worth}s need apply",
        "Your bank account should have at least {digits} digits",
        "Your wallet should be as heavy as {heavy_object}",
        "Income needed: {income} (negotiable if you're {famous})",
        "Acceptable payment methods: {payment_methods}",
        "Minimum net worth: {worth}",
        "Financial status required: {status}",
        "Suggested occupation: {job}",
        "We don't accept money, only {alternative_payment}",
        "Your credit score should be higher than {high_number}",
        "Monthly income of {income} or a {rich_relative} who loves you",
    ]
    
    # Lists of values to populate the templates
    worth_statuses = ["Billionaire", "Millionaire", "Trillionaire", "Gazillionaire", "Tech Mogul"]
    incomes = [
        "seven figures minimum", 
        "enough to buy a small island", 
        "more than the GDP of a small country",
        f"₹{price * 12 * 10:,} annually",  # 10 times annual rent
        f"₹{price * 100:,} monthly"  # Absurdly high monthly income
    ]
    digits = [7, 8, 9, 10, "infinite"]
    heavy_objects = ["a small elephant", "gold bars", "a meteorite", "the Crown Jewels"]
    famous_statuses = ["a celebrity", "royalty", "an influencer with 10M+ followers", "friends with Ambani"]
    payment_methods = [
        "gold bars, diamonds, or cryptocurrency", 
        "rare paintings or vintage cars",
        "historical artifacts or your family heirlooms"
    ]
    financial_statuses = [
        "Able to buy a yacht without checking your account balance",
        "Owns multiple private jets",
        "Has a personal chef and butler",
        "Has 'money manager' on speed dial",
        "Never looks at price tags"
    ]
    jobs = [
        "CEO of a Fortune 500 company", 
        "Tech Startup Founder with Series C funding", 
        "Bollywood Superstar",
        "International Cricket Player",
        "Heir to an ancient dynasty"
    ]
    alternative_payments = [
        "rare gems", 
        "vintage wines", 
        "NFTs of famous landmarks", 
        "shares in space exploration companies"
    ]
    high_numbers = ["800", "900", "infinity", "Pi (3.14159...)", "the number of stars in the Milky Way"]
    rich_relatives = ["generous uncle", "long-lost royal relative", "billionaire godparent"]
    
    # Choose a random phrase template
    phrase = random.choice(base_phrases)
    
    # Format the phrase with appropriate values, using `.get()` to avoid KeyError
    phrase = phrase.format(
        worth=random.choice(worth_statuses),
        income=random.choice(incomes),
        digits=random.choice(digits),
        heavy_object=random.choice(heavy_objects),
        famous=random.choice(famous_statuses),
        payment_methods=random.choice(payment_methods),
        status=random.choice(financial_statuses),
        job=random.choice(jobs),
        alternative_payment=random.choice(alternative_payments),
        high_number=random.choice(high_numbers),
        rich_relative=random.choice(rich_relatives)
    )
    
    return phrase



# Generate creative utilities responsibility statements
def generate_utilities_statement() -> str:
    """Generate a statement about utilities responsibility with humor or shade."""
    import random
    
    utilities_statements = [
        # Standard statements
        "Owner is responsible for all utilities",
        "Renter is responsible for all utilities",
        "Utilities split 50/50 between owner and renter",
        "Water included, electricity and gas paid by renter",
        
        # Humorous statements
        "Owner covers water bill (unless you take suspiciously long showers)",
        "Electricity included (up to 3 light bulbs and 1 phone charger)",
        "Utilities included (Wi-Fi password costs extra)",
        "Owner pays for utilities (terms and conditions apply in microscopic font)",
        "Utilities included on leap years only",
        "Renter responsible for utilities (owner responsible for good vibes)",
        
        # Slightly shady statements
        "Owner covers utilities on paper (additional charges may mysteriously appear)",
        "Utilities included, but AC use triggers 'climate surcharge'",
        "Water bills? Never heard of them. Electricity bills? Those are yours",
        "We'll split the utilities 30/70 - you pick which number you want!",
        "Utilities included* (*not actually included)",
        "Owner covers the utilities that work, you cover the ones that don't",
        
        # Creative alternatives
        "Electricity generated via on-site hamster wheel (maintenance your responsibility)",
        "Solar powered - pray for sunny days",
        "Water from nearby well (bucket and rope provided for nominal fee)",
        "Utilities included if you can convince the previous tenant to keep paying them",
        "All utilities provided by neighbor's unsecured Wi-Fi and extension cords",
        "Candlelight and rainwater collection encouraged to minimize utility costs",
        
        # Practical but with a twist
        "First ₹2000 of utilities covered, the rest is between you and your conscience",
        "Utilities included for first month, then we'll discuss your showering habits",
        "Utilities paid by owner (reimbursed by your security deposit)",
        "Utilities responsibility determined by monthly game of rock-paper-scissors"
    ]
    
    return random.choice(utilities_statements)


# Generate creative pet policy statements
def generate_pet_policy() -> str:
    """Generate a statement about pet policies with a mix of humor and randomness."""
    import random
    
    pet_statements = [
        # Standard statements
        "Pets allowed with a small deposit (and a promise they won't judge the neighbors).",
        "Pets allowed, but they must have better manners than the landlord's cat.",
        "Small pets allowed, as long as they don't think they're lions.",
        "Only fish are allowed, and even they must be well-behaved.",
        
        # Humorous statements
        "Pets allowed, but they must sign the lease agreement too.",
        "Pets allowed if they can contribute to rent by posing for Instagram photos.",
        "Cats allowed if they promise not to knock things over. (Good luck with that!)",
        "Dogs allowed if they can fetch the morning newspaper... from 2 miles away.",
        "Pets allowed if they can keep the landlord's parrot from spilling secrets.",
        "Only invisible pets allowed. Must be kept on invisible leashes at all times.",
        
        # Bizarre statements
        "Pets allowed, but they must pass a lie-detector test. We have trust issues.",
        "Only unicorns and dragons allowed. Proof of magical lineage required.",
        "Pets allowed if they can juggle. Bonus points for fire tricks.",
        "No pets allowed, unless they're trained in interpretive dance.",
        "Pets allowed, but they must complete a Sudoku puzzle first.",
        "Chickens allowed, but they must lay golden eggs—no exceptions.",
        
        # Shady but funny
        "Pets allowed, but we take no responsibility if they join the neighborhood gang.",
        "Only pets with five-star Yelp reviews are welcome.",
        "Pets allowed if they can teach the landlord's dog some manners.",
        "Pets allowed, but if they chase the mailman, they need to apologize personally.",
        "All pets are welcome, but the landlord's hamster is in charge. Good luck.",
        "Pets allowed, but we draw the line at pet rocks. Too much drama last time.",
        
        # Creative alternatives
        "Pets allowed if they can sing karaoke with the landlord on Fridays.",
        "Pets allowed if they can play chess. No sore losers, please.",
        "Pets allowed if they can win a staring contest with the neighbor's cat.",
        "Only pets that come with their own Netflix subscription are welcome.",
        "Pets allowed if they promise to water the plants while you're out.",
        "We accept pets, but they must have a LinkedIn profile and at least 500 connections."
    ]
    
    return random.choice(pet_statements)


def determine_property_type() -> str:
    """Randomly determine the property type."""
    property_types = ["apartment", "house", "condo", "land"]
    return random.choice(property_types)

c_type = ["buy", "rent"]

# Extract city from address
def extract_city(address: str) -> str:
    return address.split(',')[-1].strip()

# Function to create property posts
async def create_posts():
    # MongoDB connection string - replace with your actual connection string
    MONGODB_URL = "mongodb+srv://ykhare256:admin1234@cluster0.yrkd6dg.mongodb.net/real-estate?retryWrites=true&w=majority&appName=Cluster0"
    client = AsyncIOMotorClient(MONGODB_URL)
    
    # Initialize Beanie with the Post document model
    await init_beanie(database=client.real_estate, document_models=[Post])
    
    posts = []
    for idx, item in enumerate(list_data):
        # Rotate through available user IDs
        user_id = user_ids[idx % len(user_ids)]
        
        # Create post detail with random but realistic values
        post_detail = PostDetail(
            desc=f"A beautiful {item.get('bedroom')}-bedroom property in {extract_city(item.get('address'))}. "
                 f"Experience luxury living with modern amenities and a comfortable living space.",
            images=[random.choice(image_links), random.choice(image_links), random.choice(image_links)],  # Duplicating image URLs for demo
            size=800 + (idx * 100) % 500,  # Random size between 800-1300 sq ft
            school=400 + (idx * 100) % 600,  # Distance to school in meters
            bus=500 + (idx * 100) % 500,
            pet=generate_pet_policy(),
        income= generate_income_requirement(item.get('price')), 
           utilities= generate_utilities_statement(),  # Distance to bus stop in meters
            restaurant=50 + (idx * 30) % 100  # Distance to restaurant in meters
        )
        
        # Create post
        post = Post(
            title=item.get('title'),
            address=item.get('address'),
            bathroom=item.get('bathroom'),
            bedroom=item.get('bedroom'),
            city=extract_city(item.get('address')),
            img=post_detail.images[0],
            latitude=item.get('latitude'),
            longitude=item.get('longitude'),
            price=item.get('price'),
            postDetail=post_detail,
            user_id=user_id,
            p_type=determine_property_type(),
            c_type=random.choice(c_type)

        )
        
        # Add to list for bulk insert
        posts.append(post)
    
   # Insert all posts into the database
    for post in posts:
        try:
            await post.save()
            print(f"Added: {post.title}")
        except Exception as e:
            print(f"Error adding {post.title}: {e}")
    
    print(f"Successfully added {len(posts)} properties to the database")

# Run the async function
if __name__ == "__main__":
    asyncio.run(create_posts())