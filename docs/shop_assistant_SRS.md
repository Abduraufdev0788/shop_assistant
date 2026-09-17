# Software Requirements Specification — Shop Assistant

Version 0.4 · 2026-09-16 · Status: draft

## 1. Introduction

### 1.1 Purpose
Define what the Shop Assistant must do so it can be designed, built, and accepted against a fixed list of requirements. Audience: the developer (author) and the shop owner.

### 1.2 Scope
A Telegram bot that answers customers' "do you have …?" questions about a shop whose catalog is published as posts in a Telegram channel. The bot finds matching posts, replies with a link to each, and hands the conversation to the owner when it cannot answer safely.

Version 1 does **not** take orders, process payments, or manage stock.

### 1.3 Definitions
| Term | Meaning |
|---|---|
| Channel | The shop's public Telegram channel; the only source of catalog data |
| Post | One channel message: photo(s) + caption. Treated as one product |
| Product record | Structured fields extracted from a post (name, price, category, sizes, colors, keywords) |
| Filter search | Exact matching on product-record fields |
| Semantic search | Nearest-neighbour search over text embeddings of posts |
| Escalation | Forwarding a customer question to the owner and telling the customer to wait |
| Customer | Anyone who writes to the bot |
| Owner | The shop owner; receives escalations, replies through the bot |
| Admin | The developer; runs indexing and maintenance commands |

### 1.4 References
- Telegram Bot API and Telegram client API documentation

## 2. Overall Description

### 2.1 Context
```
Telegram channel ──fetch──▶ Ingestion ──▶ Product store (records + embeddings)
                                                    │
Customer ◀──Telegram bot──▶ Agent ──tools──────────┘
                              │
                              └──escalate──▶ Owner (Telegram chat)
```

### 2.2 Actors
- **Customer** — asks short questions in Uzbek (Latin or Cyrillic) or Russian, often with typos.
- **Owner** — answers escalated questions; their answer goes back to the customer.
- **Admin** — triggers re-indexing, reads logs and stats.

### 2.3 Assumptions
- A-1 The channel is @status_dokon (clothing and shoes, Tashkent, nationwide delivery); it is public.
- A-2 Posts follow a stable caption template: season tag, "Yangi model <type>", sizes line, price line, delivery note, contacts, address. At least 15 of any 20 recent posts contain a readable type, sizes and price.
- A-3 One post = one product. Multi-product posts are indexed as one record with several keywords.
- A-4 In v1 the developer acts as the owner and receives escalations in their own Telegram account.
- A-5 Post media is video; all product information needed for search is in the caption text.
- A-6 Every caption ends with the same contact/address footer, which carries no product information.

### 2.4 Constraints
- C-1 The system is built from scratch for learning purposes: no off-the-shelf agent or RAG framework may be used.
- C-2 Language model and embeddings run **locally** on the company's own GPU server (Ollama on Codeschool): no paid hosted API. Models must be multilingual (uz-Latin, uz-Cyrillic, ru).
- C-5 The bot answers only in private chats; it does not respond in groups or the channel.
- C-3 Runs unattended on a single Linux server.
- C-4 All catalog data comes from the channel; no manual product entry in v1.

## 3. Functional Requirements

### 3.1 Ingestion
| ID | Requirement |
|---|---|
| FR-1 | The system shall fetch the last N posts (default 500) from the configured channel, including caption, date, message id, and link. |
| FR-2 | The system shall skip posts with an empty caption. |
| FR-3 | The system shall detect reposts/duplicates (same caption text) and keep only the newest. |
| FR-3a | The system shall ignore the repeated contact/address footer when extracting fields and when computing similarity. |
| FR-3b | The system shall read prices written in shop notation (e.g. "980.000ming" = 980 000 so'm) and shall record a separate subscriber price when the caption marks one (e.g. "Telegram obunachilariga narx"). |
| FR-4 | For each post the system shall extract a product record: name, price (in so'm, or unknown), category, list of sizes, list of colors, list of keywords (Uzbek Latin, Uzbek Cyrillic, Russian, English synonyms). |
| FR-5 | The system shall compute and store a text embedding for each post (caption + extracted name + keywords). |
| FR-6 | The system shall store records and embeddings on disk so the bot can restart without re-indexing. |
| FR-7 | Re-running ingestion shall only process posts newer than the last indexed message id (incremental). |

### 3.2 Search
| ID | Requirement |
|---|---|
| FR-8 | The system shall support filter search on product records by any combination of: category, price range, size, color, keywords. All given filters must match. |
| FR-9 | Keyword matching shall be case-, script- (Latin/Cyrillic), and diacritic-insensitive (e.g. o' / oʻ / ў are the same letter). |
| FR-10 | When filter search returns no results and the question has a free-text part, the system shall fall back to semantic search, returning the 5 most similar posts while still honouring any price filter. |
| FR-11 | Every result shall include: name, price, post date, and post link. |
| FR-12 | The system shall answer "what's new?" questions with the most recent posts. |

### 3.3 Conversation
| ID | Requirement |
|---|---|
| FR-13 | The bot shall reply in the language of the customer's message (uz Latin, uz Cyrillic, or ru). |
| FR-14 | Every product mentioned in a reply shall be accompanied by its post link. |
| FR-15 | The bot shall never state a price, size, or availability that is not present in a retrieved record. |
| FR-16 | Posts older than 60 days (configurable) shall be presented with a "may be sold out, confirm with owner" note. |
| FR-17 | The bot shall keep conversation history per customer for the current session (in memory) so follow-ups like "qora rangi bormi?" resolve against the previous results. |
| FR-18 | The bot shall answer at most 5 products per reply; if more match, it shall ask the customer to narrow down. |

### 3.4 Escalation
| ID | Requirement |
|---|---|
| FR-19 | The system shall be able to forward a customer's question (and matched post links, if any) to the owner's chat and tell the customer the owner will reply. |
| FR-20 | The agent shall escalate when: (a) the customer asks about stock/availability, (b) both filter and semantic search return nothing relevant, (c) the customer asks about orders, delivery, payment, or anything not in the catalog. |
| FR-21 | When the owner replies to an escalation, the bot shall forward the reply to the customer. |
| FR-22 | Owner replies shall be appended to an FAQ store and be searchable by the agent in later conversations. |

### 3.5 Admin
| ID | Requirement |
|---|---|
| FR-23 | Admin shall be able to start ingestion manually from the server. |
| FR-24 | Admin shall be able to run a search from the command line without Telegram, for testing. |
| FR-25 | The bot shall log every customer question, tools called, and final answer to a file. |
| FR-26 | An admin-only `/stats` command in the bot shall report: indexed posts, last index time, questions today, escalations today. |

## 4. Non-Functional Requirements
| ID | Requirement |
|---|---|
| NFR-1 | Median reply time ≤ 8 s; 95th percentile ≤ 20 s. |
| NFR-2 | No per-question API cost (local models). A customer question shall use ≤ 8 000 input tokens on average so the GPU stays free for other services. |
| NFR-3 | Ingestion of 500 posts shall complete in ≤ 30 min on the local server with no API cost. |
| NFR-4 | No customer messages are persisted beyond the log file; no personal data is sent to the owner except the question text. |
| NFR-5 | The service restarts automatically after a crash. |
| NFR-6 | Secrets (bot token, API keys, session) are stored outside the source code and never committed to version control. |
| NFR-7 | The system is a course project: each processing stage (fetch, extract, index, search, converse, deliver) must be understandable and testable on its own. |

## 5. Out of Scope (v1)
- Orders, cart, payments, delivery tracking
- Photo-based search ("do you have this?" + image)
- Stock management or editing the catalog through the bot
- Multiple shops / channels in one deployment
- Web dashboard

## 6. Acceptance Criteria
- AC-1 An eval file of 20 realistic customer questions with expected outcome (which posts should be returned, or that the question should be escalated) exists before implementation ends.
- AC-2 ≥ 16/20 eval questions produce the expected outcome.
- AC-3 0 replies in the eval contain a price or size not present in the referenced record (FR-15).
- AC-4 At least 3 eval questions are answered correctly only via semantic search (filters alone fail), proving FR-10.
- AC-5 Owner escalation round-trip works end to end on the real bot (FR-19–21).
- AC-6 Service survives a restart with no re-indexing (FR-6).

## 7. Open Questions
| # | Question | Owner | Needed by |
|---|---|---|---|
| — | No open questions. | | |

## 8. Change Log
| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-09-16 | Initial draft |
| 0.3 | 2026-09-16 | Q-2…Q-5 closed: developer plays owner (A-4), Voyage embeddings (C-2), private chats only (C-5), 60-day threshold (FR-16) |
| 0.4 | 2026-09-17 | C-2: local models (Ollama on own GPU server) instead of Claude + Voyage; NFR-2/NFR-3 cost limits replaced by token/time limits |
| 0.2 | 2026-09-16 | Channel chosen (@status_dokon); assumptions A-1/A-2/A-5/A-6 and FR-3a/3b added from sample posts; Q-1 closed |
