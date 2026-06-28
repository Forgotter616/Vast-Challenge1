# MC1 平表说明与字段字典

本文件说明由 `MC1_final_00.json` 展平得到的两个 CSV 文件：

- `MC1_communications_flat.csv`
- `MC1_rounds_flat.csv`

两个表都由 `flatten_mc1_json.py` 生成。

## 1. MC1_communications_flat.csv

### 表用途

`MC1_communications_flat.csv` 是主分析表。

这张表的粒度是“每一条 communication 一行”。也就是说，JSON 中每条 agent 发出的消息、帖子、回复或沟通记录都会被展开为 CSV 中的一行。

适合用于：

- 分析不同 agent 的发言频率
- 分析不同 channel 的使用情况
- 构建 agent 之间的沟通网络
- 追踪某条消息如何回应上一条消息
- 对比危机前后行为变化
- 提取导致不恰当发布的事件链

### 字段说明

| 字段名 | 含义 |
| --- | --- |
| `round_index` | 当前 round 的序号，从 1 开始。用于表示数据中的第几个时间轮次。 |
| `round_hour` | 当前 round 的时间。通常是该轮事件发生的起始小时。 |
| `communication_index` | 当前 communication 在该 round 内的序号，从 1 开始。 |
| `message_id` | 消息 ID。每条 communication 的唯一标识，可用于追踪回复关系。 |
| `timestamp` | 该条 communication 的具体时间戳。通常比 `round_hour` 更精确。 |
| `agent_id` | 发出该消息的 agent 的 ID，例如 `legal_agent`、`pr_agent`。 |
| `agent_role` | 该 agent 的角色类别，例如 legal、pr、platform_trust、intern。 |
| `agent_label` | 该 agent 的显示名称，例如 Legal-Agent、PR-Agent。 |
| `channel` | 消息所在的沟通渠道，例如 `comms_huddle`、`side_huddle`、`one_on_one_chat`、`official_post`、`personal_post`、`anonymous_post`。 |
| `recipients` | 消息接收者。多个接收者用 `\|` 分隔。`ALL` 表示面向所有相关成员。 |
| `recipient_count` | 接收者数量。用于区分一对一、小范围沟通和广播。 |
| `message_type` | 消息类型，例如 broadcast、direct_message、reply 等。 |
| `responding_to` | 当前消息回复的上一条消息 ID。如果为空，表示不是直接回复某条消息。 |
| `content` | 消息正文，是最重要的文本分析字段。 |
| `declared_action` | agent 声明的行动。如果原始数据中没有该字段，则为空。 |
| `internal_reacting` | agent 内部状态中的 reacting 字段，表示即时反应或情绪性反应。 |
| `internal_rationalizing` | agent 内部状态中的 rationalizing 字段，表示其如何解释或合理化当前情况。 |
| `internal_deliberating` | agent 内部状态中的 deliberating 字段，表示其内部思考、权衡和未公开信息。 |
| `internal_state_json` | 完整的 internal_state 原始 JSON 文本。适合需要保留完整内部状态时使用。 |
| `event_headline` | 当前 round 的事件标题，概括该时间轮次的主要事件。 |
| `event_narrative` | 当前 round 的事件叙述，提供该轮环境背景和上下文。 |
| `stock_price` | 当前 round 环境中的股价字符串，例如 `$38.70`。 |
| `stock_price_num` | 清洗后的数值型股价字符串，去掉 `$`，便于导入软件后转为数字。 |
| `percent_change` | 当前 round 的股价变化百分比字符串，例如 `-0.5%`。 |
| `percent_change_num` | 清洗后的百分比变化字符串，去掉 `%` 和 `+`，便于转为数字。 |
| `market_sentiment` | 当前 round 的市场情绪，例如 neutral、low、critical 等。 |
| `trending_hashtags` | 当前 round 中出现的热门 hashtag。多个 hashtag 用 `\|` 分隔。 |
| `media_events` | 当前 round 中发生的媒体事件。多个事件用 `\|` 分隔。 |
| `social_state` | 当前 round 的社交媒体状态描述。 |
| `external_actor_actions` | 外部行动者的动作，例如媒体、客户、社交账号、监管方等外部主体的行为。 |
| `social_manager_alerts` | Social Manager 相关提醒或警报。 |
| `agents_unavailable` | 当前 round 中不可用的 agent。多个 agent 用 `\|` 分隔。 |
| `critical_deadlines` | 当前 round 中的重要截止时间或关键时间压力。 |
| `news` | 当前 round 中列出的新闻或新闻标签。多个条目用 `\|` 分隔。 |
| `communication_count` | 当前 round 中 communication 的总数量。该字段在同一个 round 的所有行中相同。 |

## 2. MC1_rounds_flat.csv

### 表用途

`MC1_rounds_flat.csv` 是 round 级摘要表。

这张表的粒度是“每一个 round/hour 一行”。它不包含单条消息正文，而是保留每个时间轮次的环境背景、市场状态、社交状态和事件摘要。

适合用于：

- 制作总时间线
- 分析股价和市场情绪变化
- 标注媒体事件和外部事件
- 对危机前、危机日进行阶段划分
- 给 communication 主表提供背景解释

### 字段说明

| 字段名 | 含义 |
| --- | --- |
| `round_index` | 当前 round 的序号，从 1 开始。 |
| `round_hour` | 当前 round 的时间。 |
| `event_headline` | 当前 round 的事件标题，用一句话概括该时间点的主要事件。 |
| `event_narrative` | 当前 round 的详细事件叙述，说明该时间段发生了什么。 |
| `stock_price` | 当前 round 的股价字符串，例如 `$38.70`。 |
| `stock_price_num` | 清洗后的股价值，去掉 `$`，便于作为数值分析。 |
| `percent_change` | 当前 round 的股价变化百分比字符串，例如 `-0.5%`。 |
| `percent_change_num` | 清洗后的百分比变化值，去掉 `%` 和 `+`，便于作为数值分析。 |
| `market_sentiment` | 当前 round 的市场情绪。 |
| `trending_hashtags` | 当前 round 中的热门 hashtag。多个条目用 `\|` 分隔。 |
| `media_events` | 当前 round 中发生的媒体事件。多个条目用 `\|` 分隔。 |
| `social_state` | 当前 round 的社交媒体整体状态。 |
| `external_actor_actions` | 当前 round 中外部行动者的行为。 |
| `social_manager_alerts` | 当前 round 中 Social Manager 相关提醒或警报。 |
| `agents_unavailable` | 当前 round 中不可用的 agent。 |
| `critical_deadlines` | 当前 round 中的重要截止时间或时间压力。 |
| `news` | 当前 round 中列出的新闻或新闻标签。 |
| `communication_count` | 当前 round 中 communication 的总数量。 |

## 两张表的关系

两张表可以通过以下字段关联：

- `round_index`
- `round_hour`

`MC1_rounds_flat.csv` 是每个时间轮次的背景摘要。

`MC1_communications_flat.csv` 是每条具体消息，并且已经把对应 round 的背景字段复制到了每一行中。因此，如果只是做普通分析，通常直接使用 `MC1_communications_flat.csv` 就够了；如果只做整体时间线或市场变化，则使用 `MC1_rounds_flat.csv` 更方便。

## 推荐使用方式

### 问题 1：事件序列和因果关系

建议主要使用：

- `MC1_rounds_flat.csv`
- `MC1_communications_flat.csv` 中的 `timestamp`、`agent_id`、`channel`、`content`、`responding_to`、`event_headline`

可以制作：

- 总时间线
- 关键决策点图
- 消息回复链
- 导致不恰当发布的路径图

### 问题 2：典型行为与异常行为对比

建议主要使用：

- `agent_id`
- `agent_role`
- `channel`
- `message_type`
- `recipient_count`
- `timestamp`
- `round_index`

可以制作：

- agent-channel 矩阵
- 危机前后发言频率对比
- 沟通网络图
- public/private channel 使用比例图

### 问题 3：先导指标

建议主要使用：

- `event_narrative`
- `media_events`
- `social_state`
- `external_actor_actions`
- `critical_deadlines`
- `market_sentiment`
- `stock_price_num`
- `percent_change_num`
- `internal_deliberating`
- `content`

可以制作：

- 风险信号时间线
- 股价和市场情绪变化图
- 早期异常行为表
- near-miss 事件对照图

## 注意事项

- `content` 是公开或半公开的消息内容；`internal_*` 字段是 agent 的内部状态，通常包含更多真实想法和隐藏背景。
- `responding_to` 可用于构建回复关系网络，但有些消息不是直接回复，因此该字段可能为空。
- `stock_price_num` 和 `percent_change_num` 目前是清洗后的字符串，导入 Python、Excel、Tableau 或其他工具后可以转为数值类型。
- 多值字段使用 `\|` 分隔，例如 `recipients`、`media_events`、`trending_hashtags`。
- 同一个 round 的环境背景字段会在 `MC1_communications_flat.csv` 中重复出现，这是为了让每条消息都能单独带上上下文，方便筛选和可视化。
