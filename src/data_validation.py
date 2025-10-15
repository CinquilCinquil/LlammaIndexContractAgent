from typing import List
from pydantic import BaseModel

"""
These classes are used to verify if the contract json
structure output by the model is correct.
"""

class Client(BaseModel):
    name: str
    email: str
    address: str
    title: str

class Developer(BaseModel):
    companyName: str
    contactPerson: str
    email: str
    address: str
    title: str

class Milestone(BaseModel):
    phase: str
    deliveryDate: str

class Deliverables(BaseModel):
    milestones: List[Milestone]
    finalDeliveryIncludes: List[str]

class Installment(BaseModel):
    percentage: str
    amountUSD: str
    condition: str

class PaymentTerms(BaseModel):
    totalProjectCostUSD: str
    installments: List[Installment]
    paymentMethod: str

class TermAndTermination(BaseModel):
    startDate: str
    duration: str
    terminationConditions: str
    paymentUponTermination: str

class Contract(BaseModel):
    agreementType: str
    effectiveDate: str
    client: Client
    developer: Developer
    scopeOfServices: List[str]
    deliverables: Deliverables
    paymentTerms: PaymentTerms
    confidentiality: List[str]
    intellectualProperty: List[str]
    termAndTermination: TermAndTermination
    governingLaw: str
    techologiesUsed: str
    SigningLocation: str

def validate_contract_json(contract_json : dict):
    Contract(**contract_json)