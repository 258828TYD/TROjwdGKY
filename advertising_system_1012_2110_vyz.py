# 代码生成时间: 2025-10-12 21:10:50
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST
from typing import List, Dict
from pydantic import BaseModel, ValidationError
from starlette.requests import Request

# Pydantic models for request and response validation
class AdCampaign(BaseModel):
    name: str
    budget: float
    target: str

class AdResponse(BaseModel):
    campaign_id: int
    name: str
    budget: float
    target: str
    status: str

# In-memory storage for ad campaigns
ad_campaigns = []
ad_campaign_id_counter = 1

# Error handler for request validation errors
async def request_validator(request: Request):
    try:
        return await request.json()
    except ValueError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="JSON body is required")

# Route for creating a new ad campaign
async def create_ad_campaign(request: Request):
    data = await request_validator(request)
    try:
        campaign = AdCampaign(**data)
    except ValidationError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    campaign.campaign_id = ad_campaign_id_counter
    ad_campaigns.append(campaign.dict())
    ad_campaign_id_counter += 1
    return JSONResponse(AdResponse(**campaign.dict()).dict())

# Route for getting all ad campaigns
async def get_ad_campaigns(request: Request):
    return JSONResponse([AdResponse(**campaign).dict() for campaign in ad_campaigns])

# Route for getting an ad campaign by ID
async def get_ad_campaign(request: Request, campaign_id: int):
    campaign = next((c for c in ad_campaigns if c['campaign_id'] == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Campaign not found")
    return JSONResponse(AdResponse(**campaign).dict())

# Main application
app = Starlette(debug=True, routes=[
    Route("/ad/campaigns", endpoint=get_ad_campaigns, methods=["GET"]),
    Route("/ad/campaigns", endpoint=create_ad_campaign, methods=["POST"]),
    Route("/ad/campaigns/{campaign_id}", endpoint=get_ad_campaign, methods=["GET"])
])

# Documentation
"""
Ad Campaign System API Documentation
================================

Endpoints:
- POST /ad/campaigns: Create a new ad campaign.
  Request body example:
    {
      "name": "New Campaign",
      "budget": 1000.0,
      "target": "New York"
    }
  Response:
    {
      "campaign_id": 1,
      "name": "New Campaign",
      "budget": 1000.0,
      "target": "New York",
      "status": "active"
    }
- GET /ad/campaigns: Get all ad campaigns.
  Response:
    [
      {
        "campaign_id": 1,
        "name": "Campaign 1",
        "budget": 1000.0,
        "target": "New York",
        "status": "active"
      }
    ]
- GET /ad/campaigns/{campaign_id}: Get an ad campaign by ID.
  Response:
    {
      "campaign_id": 1,
      "name": "Campaign 1",
      "budget": 1000.0,
      "target": "New York",
      "status": "active"
    }
"""