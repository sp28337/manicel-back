from pydantic import BaseModel


class DashboardSchema(BaseModel):
    users_total: int
    admins_total: int
    products_total: int
    crm_leads_total: int
    crm_new_leads: int


class SetAdminSchema(BaseModel):
    is_admin: bool
