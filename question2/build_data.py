#!/usr/bin/env python3
"""Build the compact, auditable data bundle used by the Task 2 report."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "MC1_communications_flat.csv"
OUTPUT = Path(__file__).resolve().parent / "q2_data.js"

PHASES = [
    {
        "id": "baseline",
        "label_en": "Historical baseline",
        "label_zh": "历史基线",
        "range_en": "Rounds 1-13 · before June 5",
        "range_zh": "第 1-13 轮 · 6 月 5 日以前",
    },
    {
        "id": "crisis",
        "label_en": "Crisis build-up",
        "label_zh": "危机积累期",
        "range_en": "Rounds 14-21 · June 5, 09:00-16:59",
        "range_zh": "第 14-21 轮 · 6 月 5 日 09:00-16:59",
    },
    {
        "id": "breach",
        "label_en": "Breach hour",
        "label_zh": "泄密小时",
        "range_en": "Round 22 · June 5, 17:00-17:59",
        "range_zh": "第 22 轮 · 6 月 5 日 17:00-17:59",
    },
    {
        "id": "post",
        "label_en": "Post-embargo",
        "label_zh": "禁发解除后",
        "range_en": "Round 23 · June 5, 18:00 onward",
        "range_zh": "第 23 轮 · 6 月 5 日 18:00 以后",
    },
]

AGENTS = [
    {
        "id": "legal_agent",
        "short": "Legal",
        "label_en": "Legal Counsel",
        "label_zh": "法务代理",
        "role_en": "Reviews legal risk and embargo compliance",
        "role_zh": "审查法律风险与禁发合规",
    },
    {
        "id": "judge_agent",
        "short": "Judge",
        "label_en": "Judge",
        "label_zh": "合规评审",
        "role_en": "Mediates conflicts and evaluates compliance",
        "role_zh": "调解冲突并评估合规性",
    },
    {
        "id": "quality_agent",
        "short": "Trust",
        "label_en": "Platform Trust",
        "label_zh": "平台信任代理",
        "role_en": "Provides governance and platform-risk evidence",
        "role_zh": "提供治理与平台风险证据",
    },
    {
        "id": "pr_agent",
        "short": "PR",
        "label_en": "PR Lead",
        "label_zh": "公关代理",
        "role_en": "Owns communications strategy and approval",
        "role_zh": "负责传播策略与审批",
    },
    {
        "id": "pr_intern_agent",
        "short": "PR Intern",
        "label_en": "PR Intern",
        "label_zh": "公关实习代理",
        "role_en": "Has access to the official TenantThread Flex account",
        "role_zh": "拥有 TenantThread 官方 Flex 账号权限",
    },
    {
        "id": "social_media_agent",
        "short": "Social",
        "label_en": "Social Manager",
        "label_zh": "社交媒体代理",
        "role_en": "Manages social messaging and amplification",
        "role_zh": "负责社交信息与传播扩散",
    },
    {
        "id": "intern_agent",
        "short": "Intern",
        "label_en": "Intern",
        "label_zh": "实习代理",
        "role_en": "Supports communications as a junior actor",
        "role_zh": "以初级角色协助传播",
    },
]

CHANNELS = [
    {
        "id": "comms_huddle",
        "label_en": "Comms huddle",
        "label_zh": "全体沟通",
        "group": "internal",
    },
    {
        "id": "one_on_one_chat",
        "label_en": "One-to-one",
        "label_zh": "一对一沟通",
        "group": "internal",
    },
    {
        "id": "side_huddle",
        "label_en": "Side huddle",
        "label_zh": "小范围协商",
        "group": "internal",
    },
    {
        "id": "official_post",
        "label_en": "Official post",
        "label_zh": "官方发帖",
        "group": "public",
    },
    {
        "id": "personal_post",
        "label_en": "Personal post",
        "label_zh": "个人发帖",
        "group": "public",
    },
    {
        "id": "anonymous_post",
        "label_en": "Anonymous post",
        "label_zh": "匿名发帖",
        "group": "public",
    },
]

PUBLIC_CHANNELS = {
    channel["id"] for channel in CHANNELS if channel["group"] == "public"
}
CHANNEL_IDS = [channel["id"] for channel in CHANNELS]
AGENT_IDS = [agent["id"] for agent in AGENTS]
PHASE_IDS = [phase["id"] for phase in PHASES]


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def phase_for(timestamp: datetime) -> str:
    crisis_day = datetime(2046, 6, 5)
    breach_start = datetime(2046, 6, 5, 17)
    embargo_end = datetime(2046, 6, 5, 18)
    if timestamp < crisis_day:
        return "baseline"
    if timestamp < breach_start:
        return "crisis"
    if timestamp < embargo_end:
        return "breach"
    return "post"


def pct(numerator: int | float, denominator: int | float) -> float:
    if not denominator:
        return 0.0
    return round(100 * numerator / denominator, 1)


def load_rows() -> list[dict]:
    with INPUT.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))

    for row in rows:
        row["_timestamp"] = parse_time(row["timestamp"])
        row["_round"] = int(row["round_index"])
        row["_recipient_count"] = int(float(row["recipient_count"] or 0))
        row["_phase"] = phase_for(row["_timestamp"])
        row["_public"] = row["channel"] in PUBLIC_CHANNELS
        row["_responding"] = bool(row["responding_to"].strip())
    return rows


def aggregate_phase_actor(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["_phase"], row["agent_id"])].append(row)

    result = []
    for phase_id in PHASE_IDS:
        for agent_id in AGENT_IDS:
            records = grouped[(phase_id, agent_id)]
            total = len(records)
            channel_counts = Counter(record["channel"] for record in records)
            public_count = sum(record["_public"] for record in records)
            side_count = channel_counts["side_huddle"]
            direct_count = channel_counts["one_on_one_chat"]
            response_count = sum(record["_responding"] for record in records)
            recipients = sum(record["_recipient_count"] for record in records)
            result.append(
                {
                    "phase": phase_id,
                    "agent": agent_id,
                    "messages": total,
                    "active": total > 0,
                    "rounds_active": len({record["_round"] for record in records}),
                    "channels": {
                        channel_id: channel_counts[channel_id]
                        for channel_id in CHANNEL_IDS
                    },
                    "channel_shares": {
                        channel_id: pct(channel_counts[channel_id], total)
                        for channel_id in CHANNEL_IDS
                    },
                    "public_count": public_count,
                    "public_share": pct(public_count, total),
                    "side_share": pct(side_count, total),
                    "direct_share": pct(direct_count, total),
                    "response_share": pct(response_count, total),
                    "avg_recipients": round(recipients / total, 2) if total else 0,
                }
            )
    return result


def aggregate_round_actor(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["_round"], row["agent_id"])].append(row)

    result = []
    for round_index in range(1, 24):
        for agent_id in AGENT_IDS:
            records = grouped[(round_index, agent_id)]
            channel_counts = Counter(record["channel"] for record in records)
            result.append(
                {
                    "round": round_index,
                    "agent": agent_id,
                    "messages": len(records),
                    "public_count": sum(record["_public"] for record in records),
                    "channels": {
                        channel_id: channel_counts[channel_id]
                        for channel_id in CHANNEL_IDS
                    },
                }
            )
    return result


def aggregate_rounds(rows: list[dict]) -> list[dict]:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["_round"]].append(row)

    result = []
    for round_index in range(1, 24):
        records = grouped[round_index]
        first = records[0]
        result.append(
            {
                "round": round_index,
                "phase": first["_phase"],
                "round_hour": first["round_hour"],
                "headline": first["event_headline"],
                "messages": len(records),
                "public_count": sum(record["_public"] for record in records),
                "active_agents": sorted({record["agent_id"] for record in records}),
            }
        )
    return result


def evidence_rows(rows: list[dict]) -> list[dict]:
    selected = []
    for row in rows:
        in_breach_hour = row["_phase"] == "breach"
        is_public = row["_public"]
        if not (in_breach_hour or is_public):
            continue
        selected.append(
            {
                "message_id": row["message_id"],
                "timestamp": row["timestamp"],
                "round": row["_round"],
                "phase": row["_phase"],
                "agent": row["agent_id"],
                "channel": row["channel"],
                "message_type": row["message_type"],
                "recipient_count": row["_recipient_count"],
                "responding_to": row["responding_to"],
                "content": row["content"],
            }
        )
    return selected


def build_bundle(rows: list[dict]) -> dict:
    phase_actor = aggregate_phase_actor(rows)
    breach_rows = [row for row in rows if row["_phase"] == "breach"]
    breach_active = sorted({row["agent_id"] for row in breach_rows})
    legal_baseline = next(
        item
        for item in phase_actor
        if item["phase"] == "baseline" and item["agent"] == "legal_agent"
    )
    legal_breach = next(
        item
        for item in phase_actor
        if item["phase"] == "breach" and item["agent"] == "legal_agent"
    )

    return {
        "meta": {
            "source": INPUT.name,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "message_count": len(rows),
            "round_count": len({row["_round"] for row in rows}),
            "agent_count": len({row["agent_id"] for row in rows}),
            "breach_message_id": "20460605_21_026",
            "breach_timestamp": "2046-06-05T17:25:00",
            "embargo_timestamp": "2046-06-05T18:00:00",
            "minutes_early": 35,
        },
        "phases": PHASES,
        "agents": AGENTS,
        "channels": CHANNELS,
        "phase_actor": phase_actor,
        "round_actor": aggregate_round_actor(rows),
        "rounds": aggregate_rounds(rows),
        "evidence": evidence_rows(rows),
        "summary": {
            "legal_baseline_public_count": legal_baseline["public_count"],
            "legal_baseline_messages": legal_baseline["messages"],
            "legal_breach_public_count": legal_breach["public_count"],
            "legal_breach_messages": legal_breach["messages"],
            "legal_breach_public_share": legal_breach["public_share"],
            "breach_active_agents": breach_active,
            "breach_active_count": len(breach_active),
            "breach_official_posts": sum(
                row["channel"] == "official_post" for row in breach_rows
            ),
        },
    }


def validate(rows: list[dict], bundle: dict) -> None:
    assert len(rows) == 912, f"Expected 912 messages, found {len(rows)}"
    assert bundle["meta"]["round_count"] == 23
    assert bundle["meta"]["agent_count"] == 7

    breach = [
        row
        for row in rows
        if row["message_id"] == bundle["meta"]["breach_message_id"]
    ]
    assert len(breach) == 1
    assert breach[0]["timestamp"] == bundle["meta"]["breach_timestamp"]
    assert breach[0]["agent_id"] == "legal_agent"
    assert breach[0]["channel"] == "personal_post"

    assert bundle["summary"]["legal_baseline_public_count"] == 0
    assert bundle["summary"]["legal_baseline_messages"] == 90
    assert bundle["summary"]["legal_breach_public_count"] == 4
    assert bundle["summary"]["legal_breach_messages"] == 28
    assert bundle["summary"]["breach_active_count"] == 3
    assert bundle["summary"]["breach_official_posts"] == 0


def main() -> None:
    rows = load_rows()
    bundle = build_bundle(rows)
    validate(rows, bundle)
    payload = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
    OUTPUT.write_text(
        "window.Q2_DATA = " + payload + ";\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)} "
        f"({len(rows)} messages, {len(bundle['evidence'])} evidence records)"
    )


if __name__ == "__main__":
    main()
