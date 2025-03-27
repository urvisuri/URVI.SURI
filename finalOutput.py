import pandas as pd

attendance_data = [
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
]
df = pd.DataFrame(attendance_data)
df["attendance_date"] = pd.to_datetime(df["attendance_date"])
df = df.sort_values(by=["student_id", "attendance_date"])
absence_streaks = []
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
                absence_streaks.append({
                    "student_id": student_id,
                    "absence_start_date": streak_start,
                    "absence_end_date": group.loc[i - 1, "attendance_date"],
                    "total_absent_days": streak_count,
                })
            streak_start = None
            streak_count = 0
    
    if streak_count > 3:
        absence_streaks.append({
            "student_id": student_id,
            "absence_start_date": streak_start,
            "absence_end_date": group.loc[len(group) - 1, "attendance_date"],
            "total_absent_days": streak_count,
        })
absence_df = pd.DataFrame(absence_streaks)
absence_df = absence_df.sort_values(by=["student_id", "absence_start_date"]).groupby("student_id").last().reset_index()
students_data = [
    {"student_id": 101, "student_name": "Alice", "parent_email": "aliceparent@gmail.com"},
    {"student_id": 102, "student_name": "Bob", "parent_email": "bob_parent@gmail.com"},
    {"student_id": 103, "student_name": "Charlie", "parent_email": None}, 
]
students_df = pd.DataFrame(students_data)
final_df = absence_df.merge(students_df, on="student_id", how="left")
def create_message(row):
    if pd.notnull(row["parent_email"]):
        start_date = row["absence_start_date"].strftime("%Y-%m-%d")
        end_date = row["absence_end_date"].strftime("%Y-%m-%d")
        return f"Dear Parent, your child {row['student_name']} was absent from {start_date} to {end_date} for {row['total_absent_days']} days. Please ensure their attendance improves."
    return None
final_df["msg"] = final_df.apply(create_message, axis=1)
final_df["msg"] = final_df["msg"].fillna("None")
final_df = final_df[["student_id", "absence_start_date", "absence_end_date", "total_absent_days", "parent_email", "msg"]]
final_df.rename(columns={"parent_email": "email"}, inplace=True)
print(final_df)
