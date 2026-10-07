from fastapi import FastAPI, Depends
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from .database import engine, Base, get_db
from . import models

# --- SEGURIDAD Y HASHING ---
import bcrypt
from jose import jwt

SECRET_KEY = "clave_super_secreta_jwt"
ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    # Hasheo directo usando bcrypt sin pasar por passlib
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=2)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- INICIALIZAR BD ---
Base.metadata.create_all(bind=engine)

# --- DEFINICIÓN DE TIPOS (GraphQL) ---
@strawberry.type
class Company:
    id: strawberry.ID
    name: str
    legalName: Optional[str]
    taxId: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    emailVerified: bool
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

@strawberry.type
class CompanyUser:
    id: strawberry.ID
    companyId: strawberry.ID
    userId: strawberry.ID
    isAdmin: bool
    isActive: bool
    joinedAt: datetime
    company: Company
    user: User

@strawberry.type
class AuthUser:
    id: strawberry.ID
    name: str
    email: str

@strawberry.type
class AuthPayload:
    token: str
    tokenType: str
    user: AuthUser

# --- INPUTS (GraphQL) ---
@strawberry.input
class CreateCompanyInput:
    name: str
    legalName: Optional[str] = None
    taxId: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

@strawberry.input
class UpdateCompanyInput:
    id: strawberry.ID
    name: Optional[str] = None
    legalName: Optional[str] = None
    taxId: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    isActive: Optional[bool] = None

@strawberry.input
class CreateCompanyAdminInput:
    companyId: strawberry.ID
    name: str
    email: str
    password: str

@strawberry.input
class CreateCompanyUserInput:
    companyId: strawberry.ID
    name: str
    email: str
    password: str

@strawberry.input
class LoginInput:
    email: str
    password: str

# --- DEPENDENCIAS ---
async def get_context(db: Session = Depends(get_db)):
    return {"db": db}

# --- QUERIES (Consultas) ---
@strawberry.type
class Query:
    @strawberry.field
    def companies(self, info: strawberry.Info, activeOnly: Optional[bool] = None) -> List[Company]:
        db = info.context["db"]
        query = db.query(models.Company)
        if activeOnly:
            query = query.filter(models.Company.is_active == True)
        db_comps = query.all()
        return [Company(id=c.id, name=c.name, legalName=c.legal_name, taxId=c.tax_id, email=c.email, phone=c.phone, isActive=c.is_active, createdAt=c.created_at, updatedAt=c.updated_at) for c in db_comps]

    @strawberry.field
    def company(self, info: strawberry.Info, id: strawberry.ID) -> Optional[Company]:
        db = info.context["db"]
        c = db.query(models.Company).filter(models.Company.id == id).first()
        if not c:
            return None
        return Company(id=c.id, name=c.name, legalName=c.legal_name, taxId=c.tax_id, email=c.email, phone=c.phone, isActive=c.is_active, createdAt=c.created_at, updatedAt=c.updated_at)

    @strawberry.field
    def companyUsers(self, info: strawberry.Info, companyId: strawberry.ID) -> List[CompanyUser]:
        db = info.context["db"]
        rels = db.query(models.CompanyUser).filter(models.CompanyUser.company_id == companyId).all()
        result = []
        for r in rels:
            c = r.company
            u = r.user
            gql_company = Company(id=c.id, name=c.name, legalName=c.legal_name, taxId=c.tax_id, email=c.email, phone=c.phone, isActive=c.is_active, createdAt=c.created_at, updatedAt=c.updated_at)
            gql_user = User(id=u.id, name=u.name, email=u.email, emailVerified=u.email_verified, isActive=u.is_active, createdAt=u.created_at, updatedAt=u.updated_at)
            result.append(CompanyUser(id=r.id, companyId=r.company_id, userId=r.user_id, isAdmin=r.is_admin, isActive=r.is_active, joinedAt=r.joined_at, company=gql_company, user=gql_user))
        return result

# --- MUTATIONS (Operaciones) ---
@strawberry.type
class Mutation:
    
    # --- CRUD EMPRESA (DÍA 1) ---
    @strawberry.mutation
    def createCompany(self, info: strawberry.Info, input: CreateCompanyInput) -> Company:
        db = info.context["db"]
        db_c = models.Company(name=input.name, legal_name=input.legalName, tax_id=input.taxId, email=input.email, phone=input.phone)
        db.add(db_c)
        db.commit()
        db.refresh(db_c)
        return Company(id=db_c.id, name=db_c.name, legalName=db_c.legal_name, taxId=db_c.tax_id, email=db_c.email, phone=db_c.phone, isActive=db_c.is_active, createdAt=db_c.created_at, updatedAt=db_c.updated_at)

    @strawberry.mutation
    def updateCompany(self, info: strawberry.Info, input: UpdateCompanyInput) -> Company:
        db = info.context["db"]
        db_c = db.query(models.Company).filter(models.Company.id == input.id).first()
        if not db_c:
            raise Exception("Empresa no encontrada")
        if input.name is not None: db_c.name = input.name
        if input.legalName is not None: db_c.legal_name = input.legalName
        if input.taxId is not None: db_c.tax_id = input.taxId
        if input.email is not None: db_c.email = input.email
        if input.phone is not None: db_c.phone = input.phone
        if input.isActive is not None: db_c.is_active = input.isActive
        db_c.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_c)
        return Company(id=db_c.id, name=db_c.name, legalName=db_c.legal_name, taxId=db_c.tax_id, email=db_c.email, phone=db_c.phone, isActive=db_c.is_active, createdAt=db_c.created_at, updatedAt=db_c.updated_at)

    @strawberry.mutation
    def deactivateCompany(self, info: strawberry.Info, id: strawberry.ID) -> Company:
        db = info.context["db"]
        db_c = db.query(models.Company).filter(models.Company.id == id).first()
        if not db_c:
            raise Exception("Empresa no encontrada")
        db_c.is_active = False
        db_c.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_c)
        return Company(id=db_c.id, name=db_c.name, legalName=db_c.legal_name, taxId=db_c.tax_id, email=db_c.email, phone=db_c.phone, isActive=db_c.is_active, createdAt=db_c.created_at, updatedAt=db_c.updated_at)

    # --- USUARIOS Y AUTENTICACIÓN (DÍA 2) ---
    @strawberry.mutation
    def createCompanyAdmin(self, info: strawberry.Info, input: CreateCompanyAdminInput) -> CompanyUser:
        db = info.context["db"]
        
        # Validar si existe la empresa
        db_c = db.query(models.Company).filter(models.Company.id == input.companyId).first()
        if not db_c: raise Exception("La empresa no existe")

        # Validar que no exista ya un admin para esta empresa
        existing_admin = db.query(models.CompanyUser).filter(models.CompanyUser.company_id == input.companyId, models.CompanyUser.is_admin == True).first()
        if existing_admin: raise Exception("La empresa ya tiene un administrador principal")

        # Validar correos duplicados
        existing_user = db.query(models.User).filter(models.User.email == input.email).first()
        if existing_user: raise Exception("El correo electrónico ya está registrado")

        hashed_pw = get_password_hash(input.password)
        new_user = models.User(name=input.name, email=input.email, hashed_password=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_cu = models.CompanyUser(company_id=db_c.id, user_id=new_user.id, is_admin=True)
        db.add(new_cu)
        db.commit()
        db.refresh(new_cu)
        
        gql_c = Company(id=db_c.id, name=db_c.name, legalName=db_c.legal_name, taxId=db_c.tax_id, email=db_c.email, phone=db_c.phone, isActive=db_c.is_active, createdAt=db_c.created_at, updatedAt=db_c.updated_at)
        gql_u = User(id=new_user.id, name=new_user.name, email=new_user.email, emailVerified=new_user.email_verified, isActive=new_user.is_active, createdAt=new_user.created_at, updatedAt=new_user.updated_at)
        return CompanyUser(id=new_cu.id, companyId=new_cu.company_id, userId=new_cu.user_id, isAdmin=new_cu.is_admin, isActive=new_cu.is_active, joinedAt=new_cu.joined_at, company=gql_c, user=gql_u)

    @strawberry.mutation
    def createCompanyUser(self, info: strawberry.Info, input: CreateCompanyUserInput) -> CompanyUser:
        db = info.context["db"]
        db_c = db.query(models.Company).filter(models.Company.id == input.companyId).first()
        if not db_c: raise Exception("La empresa no existe")

        existing_user = db.query(models.User).filter(models.User.email == input.email).first()
        if existing_user: raise Exception("El correo electrónico ya está registrado")

        hashed_pw = get_password_hash(input.password)
        new_user = models.User(name=input.name, email=input.email, hashed_password=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_cu = models.CompanyUser(company_id=db_c.id, user_id=new_user.id, is_admin=False)
        db.add(new_cu)
        db.commit()
        db.refresh(new_cu)
        
        gql_c = Company(id=db_c.id, name=db_c.name, legalName=db_c.legal_name, taxId=db_c.tax_id, email=db_c.email, phone=db_c.phone, isActive=db_c.is_active, createdAt=db_c.created_at, updatedAt=db_c.updated_at)
        gql_u = User(id=new_user.id, name=new_user.name, email=new_user.email, emailVerified=new_user.email_verified, isActive=new_user.is_active, createdAt=new_user.created_at, updatedAt=new_user.updated_at)
        return CompanyUser(id=new_cu.id, companyId=new_cu.company_id, userId=new_cu.user_id, isAdmin=new_cu.is_admin, isActive=new_cu.is_active, joinedAt=new_cu.joined_at, company=gql_c, user=gql_u)

    @strawberry.mutation
    def deactivateCompanyUser(self, info: strawberry.Info, id: strawberry.ID) -> CompanyUser:
        db = info.context["db"]
        cu = db.query(models.CompanyUser).filter(models.CompanyUser.id == id).first()
        if not cu: raise Exception("Relación no encontrada")
        cu.is_active = False
        db.commit()
        db.refresh(cu)
        
        db_c = db.query(models.Company).filter(models.Company.id == cu.company_id).first()
        db_u = db.query(models.User).filter(models.User.id == cu.user_id).first()
        gql_c = Company(id=db_c.id, name=db_c.name, legalName=db_c.legal_name, taxId=db_c.tax_id, email=db_c.email, phone=db_c.phone, isActive=db_c.is_active, createdAt=db_c.created_at, updatedAt=db_c.updated_at)
        gql_u = User(id=db_u.id, name=db_u.name, email=db_u.email, emailVerified=db_u.email_verified, isActive=db_u.is_active, createdAt=db_u.created_at, updatedAt=db_u.updated_at)
        return CompanyUser(id=cu.id, companyId=cu.company_id, userId=cu.user_id, isAdmin=cu.is_admin, isActive=cu.is_active, joinedAt=cu.joined_at, company=gql_c, user=gql_u)

    @strawberry.mutation
    def login(self, info: strawberry.Info, input: LoginInput) -> AuthPayload:
        db = info.context["db"]
        user = db.query(models.User).filter(models.User.email == input.email).first()
        if not user or not verify_password(input.password, user.hashed_password):
            raise Exception("Credenciales incorrectas")

        access_token = create_access_token(data={"sub": user.email})
        gql_user = AuthUser(id=user.id, name=user.name, email=user.email)
        return AuthPayload(token=access_token, tokenType="Bearer", user=gql_user)

# --- CONFIGURACIÓN FINAL ---
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(title="Sistema Financiero API")
app.include_router(graphql_app, prefix="/graphql")