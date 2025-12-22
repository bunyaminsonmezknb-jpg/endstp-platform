# backend/app/jobs/generate_daily_tasks.py
from __future__ import annotations

import os
import random
from dataclasses import dataclass
from datetime import datetime, date, timezone
from typing import Any, Dict, List, Optional, Tuple

# Projende zaten varsa bunu kullan:
# from app.db.session import get_supabase_admin
#
# Bu fonksiyon projeden projeye değişebiliyor.
# Sende "get_supabase_admin" var diye hatırlıyorum.
from app.db.session import get_supabase_admin  # ✅ sende vardı

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

DEFAULT_TASKS_PER_DAY = 5
DEFAULT_PUBLISH_HOUR = 10  # 10:01'de publish yapan ayrı job yazacağız (sonraki adım)
SEED_SALT = "endstp_daily_v1"


# ------------------------------------------------------------
# DATA MODELS
# ------------------------------------------------------------

@dataclass
class CandidateTopic:
    topic_id: str
    subject_id: str
    topic_name: str
    subject_name: str
    # Motor sinyalleri
    retention_rate: float          # 0-100
    days_until_forgotten: int
    difficulty_score: float        # 0-100
    priority_score: float          # 0-100 (exam weight + deficit vs)
    speed_need: float              # 0-100 (time analyzer)
    # Sentez
    gos: float                     # Görev Öncelik Skoru (0-100)
    dominant_reason: str           # retention|difficulty|speed|exam|mixed


@dataclass
class DailyTask:
    task_type: str                 # "test" | "study" | "review"
    topic_id: str
    subject_id: str
    topic_name: str
    estimated_time_minutes: int
    question_count: Optional[int]
    dominant_reason: str           # retention|difficulty|speed|exam|mixed
    source_motor: str              # "synthesis"
    priority_level: int            # 1-5


# ------------------------------------------------------------
# “AI gibi” görünen ama deterministik metin üretimi (rule-based)
# ------------------------------------------------------------

INTRO_POOL = {
    "retention": [
        "Analiz motorlarımız hafıza durumunu tekrar taradı.",
        "Bugün unutma eğrisi verilerine özellikle baktık.",
        "Son öğrenmelerinin zihinsel dayanıklılığı ölçüldü."
    ],
    "difficulty": [
        "Öğrenme profilin bugün biraz zorlayıcı bir tablo gösteriyor.",
        "Bazı konular şu an ekstra dikkat istiyor.",
        "Zorluk analiz motoru kırmızı bölgeleri işaretledi."
    ],
    "speed": [
        "Hız ve süre analizleri güncellendi.",
        "Zaman yönetiminde gelişim alanları tespit edildi.",
        "Çözüm hızın detaylı incelendi."
    ],
    "exam": [
        "Sınav öncelik motoru kritik konuları yeniden sıraladı.",
        "Sınav ağırlıkları bugün tekrar değerlendirildi.",
        "Puan getiren alanlar ve eksiklerin birlikte analiz edildi."
    ],
    "mixed": [
        "Bugün 4 motorun ortak çıktısına göre dengeli bir plan hazırlandı.",
        "Motorlar tüm verileri birleştirerek bugünün odağını belirledi.",
        "Bugün için hafıza + zorluk + sınav önceliği birlikte ele alındı."
    ],
}

REASON_POOL = {
    "retention": [
        "{topic} konusu {days} gündür tekrar edilmedi ve hafıza direnci düşüyor.",
        "{topic} bilgileri unutma eğrisinde kritik eşiğe yaklaştı.",
    ],
    "difficulty": [
        "{topic} senin için yüksek zorluk bölgesinde.",
        "{topic} konusunda öğrenme yükün ortalamanın üzerinde.",
    ],
    "speed": [
        "{topic} için hedef hız seviyesine yaklaşmanı istiyoruz.",
        "Bu görev {topic} konusunda süre yönetimini güçlendirmek için seçildi.",
    ],
    "exam": [
        "{topic}, sınavda yüksek ağırlığa sahip ve net kazancı potansiyeli yüksek.",
        "{topic} puan getiren alanlardan; bugün bu yüzden öne alındı.",
    ],
    "mixed": [
        "{topic} hem unutma riski hem de sınav önceliği nedeniyle üst sırada.",
        "{topic} çoklu sinyal verdi (hafıza + zorluk + öncelik).",
    ]
}

ACTION_POOL = {
    "retention": [
        "{t} dakikalık kısa bir tekrar büyük fark yaratır.",
        "Bugün küçük bir tekrar, yarın daha sağlam net demek."
    ],
    "difficulty": [
        "Bugün acele etmeden derinleşmeni istiyoruz.",
        "Bu konuyu sakin ve odaklı çalış; tempo sonra gelir."
    ],
    "speed": [
        "Hedefimiz bu işi {t} dakikada bitirmen.",
        "Süreyi biraz zorlayarak ilerle; hız kası böyle gelişir."
    ],
    "exam": [
        "Bugün bu görevi tamamlamak seni sınav çizgisine yaklaştırır.",
        "Bu alanı toparlamak net getirisini hızlandırır."
    ],
    "mixed": [
        "Bugün bu görevi bitirmen genel planı hızlandıracak.",
        "Bu görev tamamlanınca sonraki konular daha rahat akacak."
    ],
}

CLOSING_POOL = [
    "Kontrol sende. Başla!",
    "Küçük adımlar büyük sonuçlar getirir.",
    "Akşam verilerini girince gelişimini birlikte göreceğiz.",
    "Bugünkü çaban yarının rahatlığı olacak."
]


def _seeded_choice(items: List[str], seed: str) -> str:
    rnd = random.Random(seed)
    return items[rnd.randrange(0, len(items))]


def build_daily_motivation(student_name: str, tasks: List[DailyTask], plan_date: date) -> Dict[str, Any]:
    """
    Deterministic + değişken görünen metin:
    seed = student + date + salt
    """
    if not tasks:
        return {
            "text": f"Günaydın {student_name}! Bugün için yeni görev bulunamadı. İstersen geçmiş eksiklerine odaklanalım.",
            "dominant_reason": "mixed",
        }

    # dominant: en yüksek priority_level içinden reason
    top = sorted(tasks, key=lambda t: (t.priority_level, t.estimated_time_minutes), reverse=True)[0]
    dominant = top.dominant_reason if top.dominant_reason in INTRO_POOL else "mixed"

    seed_base = f"{SEED_SALT}:{student_name}:{plan_date.isoformat()}:{dominant}"

    intro = _seeded_choice(INTRO_POOL[dominant], seed_base + ":intro")
    closing = _seeded_choice(CLOSING_POOL, seed_base + ":closing")

    # 1-2 görev üzerinden örnekleme
    sample_tasks = tasks[:2]
    reason_parts = []
    action_parts = []

    for idx, t in enumerate(sample_tasks, start=1):
        r = t.dominant_reason if t.dominant_reason in REASON_POOL else "mixed"
        reason_tpl = _seeded_choice(REASON_POOL[r], seed_base + f":reason:{idx}")
        action_tpl = _seeded_choice(ACTION_POOL[r], seed_base + f":action:{idx}")

        reason_parts.append(
            "• " + reason_tpl.format(topic=t.topic_name, days=3)  # days gerçek değer B adımında DB’den gelecek
        )
        action_parts.append(
            action_tpl.format(t=t.estimated_time_minutes, topic=t.topic_name)
        )

    text = (
        f"GÜNAYDIN {student_name}! 👋\n\n"
        f"{intro}\n\n"
        "Bugün öncelikli odakların:\n"
        + "\n".join(reason_parts)
        + "\n\n"
        + " ".join(action_parts)
        + "\n\n"
        + closing
    )

    return {
        "text": text,
        "dominant_reason": dominant
    }


# ------------------------------------------------------------
# Task seçimi (kural motoru)
# ------------------------------------------------------------

def choose_tasks_from_candidates(cands: List[CandidateTopic], tasks_per_day: int = DEFAULT_TASKS_PER_DAY) -> List[DailyTask]:
    """
    Basit ama güçlü kural:
    - En yüksek GÖS'ten başla
    - reason'a göre task type seç
    - süre/soru hedefi koy
    """
    if not cands:
        return []

    cands_sorted = sorted(cands, key=lambda c: c.gos, reverse=True)
    selected: List[DailyTask] = []

    for c in cands_sorted[:tasks_per_day]:
        # reason -> task_type
        if c.dominant_reason == "retention":
            task_type = "review"
            est = 15
            q = None
        elif c.dominant_reason == "speed":
            task_type = "test"
            est = 15
            q = 12
        elif c.dominant_reason == "difficulty":
            task_type = "study"
            est = 30
            q = None
        elif c.dominant_reason == "exam":
            task_type = "test"
            est = 20
            q = 12
        else:
            task_type = "study"
            est = 20
            q = None

        # priority_level (1-5)
        if c.gos >= 85:
            pl = 5
        elif c.gos >= 70:
            pl = 4
        elif c.gos >= 55:
            pl = 3
        elif c.gos >= 40:
            pl = 2
        else:
            pl = 1

        selected.append(
            DailyTask(
                task_type=task_type,
                topic_id=c.topic_id,
                subject_id=c.subject_id,
                topic_name=c.topic_name,
                estimated_time_minutes=est,
                question_count=q,
                dominant_reason=c.dominant_reason,
                source_motor="synthesis",
                priority_level=pl,
            )
        )

    return selected


# ------------------------------------------------------------
# DB ADAPTER (B adımında SQL ile tamamlanacak)
# ------------------------------------------------------------

def fetch_active_students(supabase) -> List[Dict[str, Any]]:
    """
    Beklenen tablo: students (id, full_name, is_active)
    Eğer sende farklıysa B adımında uyarlayacağız.
    """
    res = supabase.table("students").select("id, full_name").eq("is_active", True).execute()
    return res.data or []


def fetch_daily_candidates(supabase, student_id: str, plan_date: date) -> List[CandidateTopic]:
    """
    ✅ B adımında yazacağımız RPC:
    rpc_get_daily_task_candidates(p_student_id uuid, p_date date)
    Dönen kolonlar:
      topic_id, subject_id, topic_name, subject_name,
      retention_rate, days_until_forgotten, difficulty_score, priority_score, speed_need,
      gos, dominant_reason
    """
    rpc_res = supabase.rpc(
        "rpc_get_daily_task_candidates",
        {"p_student_id": student_id, "p_date": plan_date.isoformat()},
    ).execute()

    rows = rpc_res.data or []
    out: List[CandidateTopic] = []
    for r in rows:
        out.append(
            CandidateTopic(
                topic_id=str(r["topic_id"]),
                subject_id=str(r["subject_id"]),
                topic_name=str(r["topic_name"]),
                subject_name=str(r.get("subject_name", "")),
                retention_rate=float(r.get("retention_rate", 0)),
                days_until_forgotten=int(r.get("days_until_forgotten", 0)),
                difficulty_score=float(r.get("difficulty_score", 0)),
                priority_score=float(r.get("priority_score", 0)),
                speed_need=float(r.get("speed_need", 0)),
                gos=float(r.get("gos", 0)),
                dominant_reason=str(r.get("dominant_reason", "mixed")),
            )
        )
    return out


def upsert_daily_plan(supabase, student_id: str, plan_date: date, motivation: Dict[str, Any]) -> str:
    """
    ✅ B adımında yazacağımız tablo:
    student_daily_plans (id uuid, student_id uuid, plan_date date, motivation_text text, dominant_reason text, status text, created_at)
    """
    payload = {
        "student_id": student_id,
        "plan_date": plan_date.isoformat(),
        "motivation_text": motivation["text"],
        "dominant_reason": motivation.get("dominant_reason", "mixed"),
        "status": "draft",  # publish job (10:01) bunu published yapacak
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    res = supabase.table("student_daily_plans").upsert(payload, on_conflict="student_id,plan_date").select("id").execute()
    plan_id = res.data[0]["id"]
    return str(plan_id)


def replace_plan_tasks(supabase, plan_id: str, student_id: str, plan_date: date, tasks: List[DailyTask]) -> None:
    """
    ✅ B adımında yazacağımız tablo:
    student_tasks (id uuid, plan_id uuid, student_id uuid, task_date date, task_type text,
                  topic_id uuid, subject_id uuid, topic_name text,
                  source_motor text, priority_level int,
                  estimated_time_minutes int, question_count int null,
                  status text, completed_at timestamptz null, manual_completion bool)
    """
    # 1) O günün eski task'larını sil
    supabase.table("student_tasks").delete().eq("student_id", student_id).eq("task_date", plan_date.isoformat()).execute()

    # 2) Yenileri insert
    rows = []
    for t in tasks:
        rows.append(
            {
                "plan_id": plan_id,
                "student_id": student_id,
                "task_date": plan_date.isoformat(),
                "task_type": t.task_type,
                "topic_id": t.topic_id,
                "subject_id": t.subject_id,
                "topic_name": t.topic_name,
                "source_motor": t.source_motor,
                "priority_level": int(t.priority_level),
                "estimated_time_minutes": int(t.estimated_time_minutes),
                "question_count": t.question_count,
                "status": "pending",
                "completed_at": None,
                "manual_completion": False,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "dominant_reason": t.dominant_reason,
            }
        )

    if rows:
        supabase.table("student_tasks").insert(rows).execute()


# ------------------------------------------------------------
# MAIN JOB
# ------------------------------------------------------------

def generate_daily_tasks_for_date(plan_date: Optional[date] = None) -> Dict[str, Any]:
    """
    CRON burayı çağıracak.
    """
    supabase = get_supabase_admin()
    plan_date = plan_date or datetime.now(timezone.utc).date()

    students = fetch_active_students(supabase)

    summary = {
        "date": plan_date.isoformat(),
        "students_total": len(students),
        "students_planned": 0,
        "students_failed": 0,
        "errors": [],
    }

    for s in students:
        student_id = str(s["id"])
        student_name = str(s.get("full_name") or "Öğrenci")

        try:
            # 1) adaylar (4 motor sentezi) -> RPC
            cands = fetch_daily_candidates(supabase, student_id, plan_date)

            # 2) task seçimi
            tasks = choose_tasks_from_candidates(cands, tasks_per_day=DEFAULT_TASKS_PER_DAY)

            # 3) motivasyon
            motivation = build_daily_motivation(student_name, tasks, plan_date)

            # 4) plan upsert
            plan_id = upsert_daily_plan(supabase, student_id, plan_date, motivation)

            # 5) tasks replace
            replace_plan_tasks(supabase, plan_id, student_id, plan_date, tasks)

            summary["students_planned"] += 1

        except Exception as e:
            summary["students_failed"] += 1
            summary["errors"].append({"student_id": student_id, "error": str(e)})

    return summary


if __name__ == "__main__":
    # CLI run: python -m app.jobs.generate_daily_tasks
    result = generate_daily_tasks_for_date()
    print(result)
