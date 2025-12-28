#!/usr/bin/env python3
"""
Motor Activity Stats Viewer
logs/motor_activity.log dosyasını analiz eder
"""
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

log_file = Path("logs/motor_activity.log")

if not log_file.exists():
    print("❌ Henüz log dosyası yok. Motor çağrısı yapılmamış.")
    exit(1)

# Log'ları oku
logs = []
with open(log_file, 'r') as f:
    for line in f:
        try:
            logs.append(json.loads(line.strip()))
        except:
            pass

if not logs:
    print("❌ Log dosyası boş.")
    exit(1)

print("=" * 60)
print("🔍 MOTOR AKTİVİTE RAPORU")
print("=" * 60)
print(f"Toplam Kayıt: {len(logs)}")
print(f"İlk Kayıt: {logs[0]['timestamp']}")
print(f"Son Kayıt: {logs[-1]['timestamp']}")
print()

# Motor bazında grupla
by_motor = defaultdict(lambda: {"v1": 0, "v2": 0, "fallback": 0, "total_time": 0})

for log in logs:
    motor = log["motor_type"]
    version = log["version"]
    
    by_motor[motor][version] += 1
    by_motor[motor]["total_time"] += log["execution_time_ms"]
    
    if log["fallback_used"]:
        by_motor[motor]["fallback"] += 1

print("📊 MOTOR BAZINDA İSTATİSTİKLER:")
print("-" * 60)

for motor, stats in by_motor.items():
    total = stats["v1"] + stats["v2"]
    avg_time = stats["total_time"] / total if total > 0 else 0
    
    print(f"\n🔧 {motor.upper()}")
    print(f"   v1 çağrıldı: {stats['v1']:4d} kez")
    print(f"   v2 çağrıldı: {stats['v2']:4d} kez")
    print(f"   Fallback:   {stats['fallback']:4d} kez")
    print(f"   Avg Time:   {avg_time:6.2f}ms")

# Tier bazında
print("\n" + "=" * 60)
print("👥 TİER BAZINDA:")
print("-" * 60)

by_tier = defaultdict(int)
for log in logs:
    by_tier[log["user_tier"]] += 1

for tier, count in sorted(by_tier.items()):
    print(f"   {tier:10s}: {count:4d} çağrı")

# Son 10 çağrı
print("\n" + "=" * 60)
print("🕐 SON 10 MOTOR ÇAĞRISI:")
print("-" * 60)

for log in logs[-10:]:
    time = datetime.fromisoformat(log["timestamp"]).strftime("%H:%M:%S")
    motor = log["motor_type"][:8]
    version = log["version"]
    tier = log["user_tier"][:4]
    ms = log["execution_time_ms"]
    fallback = "⚠️" if log["fallback_used"] else "✅"
    
    print(f"{time} | {motor:8s} | v{version} | {tier:4s} | {ms:6.1f}ms | {fallback}")

print("\n" + "=" * 60)
