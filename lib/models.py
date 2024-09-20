from sqlalchemy import ForeignKey, Column, Integer,Boolean, String, MetaData, create_engine
from sqlalchemy.orm import relationship,sessionmaker,  backref
from sqlalchemy.orm import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean, default=False)
    role_id = Column(Integer(), ForeignKey('roles.id'))
    
    engine = create_engine('sqlite:///theater.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    def __repr__(self):
        return f'Audition(id={self.id}, ' + \
            f'actor={self.actor}, ' + \
            f'role_id={self.role_id})'
    
    def call_back(self):
        self.hired = True
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    character_name = Column(String())

    def __repr__(self):
        return f'Role(id={self.id}, ' + \
            f'character_name={self.character_name})'    
    
    auditions = relationship('Audition', backref='role')

    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]

   
    def lead(self):
        lead_audition = next((audition for audition in self.auditions if audition.hired), None)
        return lead_audition or 'no actor has been hired for this role'
    
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else 'no actor has been hired for understudy for this role'
    
