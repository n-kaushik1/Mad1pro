
# Mad1pro

**Mad1pro** is a web platform designed to facilitate connections between sponsors and influencers. Sponsors can promote their products or services, while influencers can gain financial benefits by endorsing these offerings.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Frameworks and Technologies](#frameworks-and-technologies)
- [Database Schema](#database-schema)
- [Roles and Responsibilities](#roles-and-responsibilities)
- [Installation](#installation)
- [Demo](#demo)

## Project Overview
This platform is built to coordinate influencer marketing campaigns, allowing sponsors to create and manage advertising campaigns, while influencers can accept or reject offers based on their preferences.

## Features
- **Admin:**
  - Monitor users and campaigns
  - View statistics and manage flagged content
- **Sponsors:**
  - Create, update, and manage campaigns
  - Search for influencers and track progress
  - Accept influencer requests for public campaigns
- **Influencers:**
  - Receive and respond to ad requests
  - Search for public campaigns
  - Manage profile and view campaign progress

## Frameworks and Technologies
- **Flask**: Handles web requests and routing.
- **Jinja2 + Bootstrap**: Front-end rendering and styling.
- **SQLite**: Database for storing platform data.
- **Flask SQLAlchemy**: ORM for interacting with the database.

## Database Schema
1. **Admin_Info**: Stores admin login details.
2. **Influencer_Info**: Information about influencers including username, platform, followers, and niche.
3. **Sponsor_Info**: Contains sponsor details, such as industry and flagged status.
4. **Campaign_Info**: Campaign details, including name, budget, and goals.
5. **Adrequest_Info**: Manages ad requests, including payment and status.

## Roles and Responsibilities
- **Admin**: Has complete control over the platform and its users.
- **Sponsors**: Advertise products through influencer campaigns.
- **Influencers**: Promote products and earn through campaigns.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Mad1pro.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    python app.py
    ```

## Demo
A video demo is available [here](https://drive.google.com/file/d/1n4XmXRWEKd0unpUx4Gq2x98lKSRG2mwM/view?usp=sharing).

