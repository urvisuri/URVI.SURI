import pandas as pd

data = [
    {"student_id": 101, "attendance_date": "2024-03-01", "status": "Absent"},
    {"student_id": 101, "attendance_date": "2024-03-02", "status": "Absent"},
    {"student_id": 101, "attendance_date": "2024-03-03", "status": "Absent"},
    {"student_id": 101, "attendance_date": "2024-03-04", "status": "Absent"},
    {"student_id": 101, "attendance_date": "2024-03-05", "status": "Present"},
    {"student_id": 102, "attendance_date": "2024-03-02", "status": "Absent"},
    {"student_id": 102, "attendance_date": "2024-03-03", "status": "Absent"},
    {"student_id": 102, "attendance_date": "2024-03-04", "status": "Absent"},
    {"student_id": 102, "attendance_date": "2024-03-05", "status": "Absent"},
    {"student_id": 103, "attendance_date": "2024-03-05", "status": "Absent"},
    {"student_id": 103, "attendance_date": "2024-03-06", "status": "Absent"},
    {"student_id": 103, "attendance_date": "2024-03-07", "status": "Absent"},
    {"student_id": 103, "attendance_date": "2024-03-08", "status": "Absent"},
    {"student_id": 103, "attendance_date": "2024-03-09", "status": "Absent"},
    {"student_id": 104, "attendance_date": "2024-03-01", "status": "Present"},
    {"student_id": 104, "attendance_date": "2024-03-02", "status": "Present"},
    {"student_id": 104, "attendance_date": "2024-03-03", "status": "Absent"},
    {"student_id": 104, "attendance_date": "2024-03-04", "status": "Present"},
    {"student_id": 104, "attendance_date": "2024-03-05", "status": "Present"},
]
df = pd.DataFrame(data)
df["attendance_date"] = pd.to_datetime(df["attendance_date"])
df = df.sort_values(by=["student_id", "attendance_date"])
result = []
for student_id, group in df.groupby("student_id"):
    group = group.reset_index(drop=True)
    streak_start = None
    streak_count = 0   
    for i in range(len(group)):
        if group.loc[i, "status"] == "Absent":
            if streak_start is None:
                streak_start = group.loc[i, "attendance_date"]
            streak_count += 1
        else:
            if streak_count > 3:
                result.append({
                    "student_id": student_id,
                    "absence_start_date": streak_start,
                    "absence_end_date": group.loc[i - 1, "attendance_date"],
                    "total_absent_days": streak_count,
                })
            streak_start = None
            streak_count = 0
    if streak_count > 3:
        result.append({
            "student_id": student_id,
            "absence_start_date": streak_start,
            "absence_end_date": group.loc[len(group) - 1, "attendance_date"],
            "total_absent_days": streak_count,
        })
absent_streaks_df = pd.DataFrame(result)
latest_streak_df = absent_streaks_df.sort_values(by=["student_id", "absence_start_date"]).groupby("student_id").last().reset_index()
print(latest_streak_df)
