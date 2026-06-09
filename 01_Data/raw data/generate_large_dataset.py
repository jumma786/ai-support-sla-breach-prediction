#!/usr/bin/env python3
"""
Generate a large synthetic AI Support Operations dataset.

Recommended classroom commands:
    python generate_large_dataset.py --rows 100000 --output support_sla_100k.csv
    python generate_large_dataset.py --rows 5000000 --output support_sla_full_5m.csv

A 5,000,000-row file with the text column included is designed to simulate
real-world scale and can exceed 1GB depending on platform, quoting and line endings.
Use --chunk-size to control memory usage.
"""
import argparse
import csv
import datetime
import random
import math

REGIONS = ["London", "Greater Manchester", "West Midlands", "Scotland", "Wales", "Northern Ireland", "South East", "South West", "Yorkshire", "East Midlands"]
SEGMENTS = ["SMB", "Mid-Market", "Enterprise", "Public Sector"]
CHANNELS = ["Email", "Web", "Phone", "Chat", "Partner Portal"]
CHANNEL_DIRTY = ["email", "E-mail", "WEB", "chat ", "Phone", "Partner portal", "Partner Portal", "Web", "Email"]
PRODUCT_AREAS = ["Billing", "Payments", "Account Access", "API Integration", "Data Export", "Security", "Reporting", "Mobile App", "Workflow Automation"]
ISSUE_CATEGORIES = ["bug", "how_to", "billing_query", "access_request", "service_outage", "integration_failure", "data_quality", "performance", "refund_request"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
AGENTS = ["Ava", "Oliver", "Noah", "Isla", "Muhammad", "Amelia", "George", "Grace", "Leo", "Mia", "Sophie", "Harry"]
MESSAGE_TEMPLATES = [
    "Customer reports {issue} in {product}. They need help because {impact}.",
    "The user cannot complete a workflow in {product}. Error appears during {issue}.",
    "Client asks for urgent support regarding {issue}; impact: {impact}.",
    "Ticket raised through support queue for {product}; customer notes {issue} and asks for next steps.",
    "Account team escalated a customer case connected to {product}. Main issue: {issue}.",
]
IMPACTS = [
    "monthly reporting is delayed", "payment processing is blocked", "a senior stakeholder is waiting",
    "several end users are affected", "the renewal review is due", "an integration partner is blocked",
    "the customer is threatening cancellation", "a compliance deadline is near", "the issue affects only one user"
]
URGENT_WORDS = ["urgent", "ASAP", "immediately", "blocked", "critical", "escalate", "deadline"]
REFUND_WORDS = ["refund", "credit", "chargeback", "invoice correction", "billing dispute"]

FIELDNAMES = [
    "ticket_id","account_id","customer_segment","uk_region","support_channel","product_area",
    "issue_category","priority_initial","submitted_at","day_of_week","hour_of_day",
    "customer_tenure_months","contract_value_gbp","previous_tickets_90d","avg_sentiment_score",
    "customer_message","message_length","contains_urgent_keyword","contains_refund_keyword",
    "agent_queue_length_at_submit","assigned_agent","agent_experience_months","backlog_age_hours",
    "first_response_minutes","reopened_last_90d","resolved_at","escalated_prior_to_resolution",
    "resolution_hours","final_priority","sla_breached"
]

def clamp(x, a, b):
    return max(a, min(b, x))

def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]

def make_row(i, start_date):
    ticket_id = f"TCK-{202500000+i:09d}"
    account_id = f"ACC-{random.randint(10000,99999)}"
    segment = weighted_choice(SEGMENTS, [45,30,18,7])
    region = random.choice(REGIONS)
    if random.random() < 0.04:
        region = region.lower() + (" " if random.random()<0.5 else "")
    channel = weighted_choice(CHANNELS, [30, 28, 17, 20, 5])
    if random.random() < 0.08:
        channel = random.choice(CHANNEL_DIRTY)
    product = weighted_choice(PRODUCT_AREAS, [14,12,13,10,8,8,12,10,13])
    if random.random() < 0.03:
        product = product.lower()
    issue = weighted_choice(ISSUE_CATEGORIES, [18,15,12,10,9,10,10,10,6])
    submitted = start_date + datetime.timedelta(minutes=random.randint(0, 180*24*60))
    hour = submitted.hour
    dow = submitted.strftime("%A")
    tenure = int(max(0, random.gauss(28, 18)))
    contract_value = round(max(1200, random.lognormvariate(9.5, 0.75)), 2)
    if segment == "Enterprise":
        contract_value *= random.uniform(2.5, 7.5)
    elif segment == "Public Sector":
        contract_value *= random.uniform(2, 5)
    elif segment == "SMB":
        contract_value *= random.uniform(0.4, 1.2)
    if random.random() < 0.003:
        contract_value *= random.uniform(20, 60)
    previous_tickets = max(0, int(random.expovariate(1/3)))
    sentiment = clamp(random.gauss(0.05, 0.52), -1, 1)
    if issue in ["service_outage", "refund_request", "integration_failure"]:
        sentiment -= random.uniform(0.1, 0.45)
    sentiment = round(clamp(sentiment, -1, 1), 3)
    queue_len = max(0, int(random.gauss(30, 16)))
    if hour in [9,10,11,14,15,16]:
        queue_len += random.randint(5, 25)
    if random.random() < 0.004:
        queue_len = -random.randint(1,5)
    agent_exp = max(1, int(random.gauss(20, 14)))
    backlog_age = max(0, random.expovariate(1/8))
    if random.random() < 0.02:
        backlog_age *= random.uniform(5, 15)
    contains_urgent = int(issue in ["service_outage", "integration_failure"] or random.random() < 0.12)
    contains_refund = int(issue in ["refund_request", "billing_query"] and random.random() < 0.35)
    impact = random.choice(IMPACTS)
    message = random.choice(MESSAGE_TEMPLATES).format(issue=issue.replace("_"," "), product=product, impact=impact)
    if contains_urgent:
        message += " " + random.choice(URGENT_WORDS) + "."
    if contains_refund:
        message += " Customer mentions " + random.choice(REFUND_WORDS) + "."
    # Pad a minority of messages to create a more realistic, larger file footprint.
    if random.random() < 0.18:
        message += " " + ("Additional context: customer has provided screenshots and repeated reproduction steps. " * random.randint(1, 5))
    msg_len = len(message)

    priority_seed = weighted_choice(PRIORITIES, [30,42,20,8])
    base_resolution = 8 + (queue_len*0.16) + (previous_tickets*0.8) + (backlog_age*0.45) - (agent_exp*0.08)
    base_resolution += {"Low":0,"Medium":2,"High":5,"Critical":8}[priority_seed]
    issue_factor = {
        "bug": 4, "how_to": -2, "billing_query": 1, "access_request": -1, "service_outage": 10,
        "integration_failure": 9, "data_quality": 6, "performance": 5, "refund_request": 3
    }[issue]
    seg_factor = {"SMB":0, "Mid-Market":2, "Enterprise":4, "Public Sector":5}[segment]
    resolution = max(0.3, random.gauss(base_resolution + issue_factor + seg_factor, 7))
    first_response = max(1, int(random.gauss(60 + queue_len*2.8 - agent_exp*0.7 + contains_urgent*25, 70)))

    priority_score = (
        0.001*contract_value + previous_tickets*2 + queue_len*0.6 + backlog_age*1.5
        + contains_urgent*25 + contains_refund*6 - sentiment*15 + issue_factor*2 + seg_factor*3
    )
    priority_initial = "Low"
    if priority_score > 80:
        priority_initial = "Critical"
    elif priority_score > 50:
        priority_initial = "High"
    elif priority_score > 25:
        priority_initial = "Medium"
    if random.random() < 0.08:
        priority_initial = random.choice(PRIORITIES)

    sla_limit = {"Low":72, "Medium":48, "High":24, "Critical":8}[priority_initial]
    if segment in ["Enterprise","Public Sector"]:
        sla_limit *= 0.85
    breached = int(resolution > sla_limit or first_response > (sla_limit*60*0.5))
    escalated_post = int(breached or (priority_initial in ["High","Critical"] and random.random()<0.35))
    final_priority = priority_initial
    if breached and priority_initial in ["Low","Medium"] and random.random()<0.65:
        final_priority = "High"
    if breached and random.random()<0.25:
        final_priority = "Critical"
    resolved_at = submitted + datetime.timedelta(hours=resolution)

    row = {
        "ticket_id": ticket_id, "account_id": account_id, "customer_segment": segment,
        "uk_region": region, "support_channel": channel, "product_area": product,
        "issue_category": issue, "priority_initial": priority_initial,
        "submitted_at": submitted.strftime("%Y-%m-%d %H:%M:%S"), "day_of_week": dow,
        "hour_of_day": hour, "customer_tenure_months": tenure,
        "contract_value_gbp": round(contract_value, 2), "previous_tickets_90d": previous_tickets,
        "avg_sentiment_score": sentiment, "customer_message": message, "message_length": msg_len,
        "contains_urgent_keyword": contains_urgent, "contains_refund_keyword": contains_refund,
        "agent_queue_length_at_submit": queue_len, "assigned_agent": random.choice(AGENTS),
        "agent_experience_months": agent_exp, "backlog_age_hours": round(backlog_age, 2),
        "first_response_minutes": first_response, "reopened_last_90d": int(random.random() < (0.04 + 0.015*previous_tickets)),
        "resolved_at": resolved_at.strftime("%Y-%m-%d %H:%M:%S"),
        "escalated_prior_to_resolution": escalated_post, "resolution_hours": round(resolution, 2),
        "final_priority": final_priority, "sla_breached": breached,
    }
    # Intentional data quality issues.
    if random.random() < 0.025: row["avg_sentiment_score"] = ""
    if random.random() < 0.018: row["customer_tenure_months"] = ""
    if random.random() < 0.014: row["product_area"] = ""
    if random.random() < 0.012: row["priority_initial"] = ""
    if random.random() < 0.006: row["submitted_at"] = ""
    return row

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=1000000)
    parser.add_argument("--output", type=str, default="support_sla_large_dataset.csv")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--chunk-size", type=int, default=100000)
    parser.add_argument("--duplicate-rate", type=float, default=0.006)
    args = parser.parse_args()
    random.seed(args.seed)
    start_date = datetime.datetime(2025, 9, 1, 0, 0)

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        buffer = []
        for i in range(args.rows):
            row = make_row(i, start_date)
            writer.writerow(row)
            if random.random() < args.duplicate_rate:
                buffer.append(row)
            if (i + 1) % args.chunk_size == 0:
                for dup in buffer:
                    writer.writerow(dup)
                buffer = []
                print(f"Wrote approximately {i+1:,} base rows...")
        for dup in buffer:
            writer.writerow(dup)
    print(f"Done. Wrote dataset to {args.output}")

if __name__ == "__main__":
    main()
