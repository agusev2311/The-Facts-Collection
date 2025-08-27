from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import config

# База для моделей
Base = declarative_base()

# Движок для подключения к PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{config.db['user']}:{config.db['password']}@"
    f"{config.db['host']}:{config.db['port']}/{config.db['database']}"
)

# Сессия для работы с базой
SessionLocal = sessionmaker(bind=engine)

print("created")