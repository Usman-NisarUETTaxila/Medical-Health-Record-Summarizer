#!/usr/bin/env python3
"""
Direct database fix to remove NOT NULL constraints
"""
import sqlite3
import os
import shutil

def fix_database_constraints():
    """Remove NOT NULL constraints from database"""
    
    db_path = os.path.join('patient_system', 'db.sqlite3')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found.")
        return
    
    # Create backup
    backup_path = db_path + '.backup'
    shutil.copy2(db_path, backup_path)
    print(f"✅ Database backed up to {backup_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Fixing database constraints...")
        
        # For SQLite, we need to recreate tables without NOT NULL constraints
        # First, let's check current schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='patients_treatmentplan'")
        result = cursor.fetchone()
        
        if result:
            print("📋 Current TreatmentPlan table schema:")
            print(result[0])
            
            # Create new table without NOT NULL constraints
            cursor.execute("""
                CREATE TABLE patients_treatmentplan_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL REFERENCES patients_patient(id),
                    checkup_id INTEGER REFERENCES patients_checkup(id),
                    related_disease VARCHAR(100),
                    assigned_doctor VARCHAR(100),
                    prescribed_medications TEXT,
                    procedures TEXT,
                    next_followup_date DATE,
                    lifestyle_recommendations TEXT,
                    physiotherapy_advice TEXT
                )
            """)
            
            # Copy existing data
            cursor.execute("""
                INSERT INTO patients_treatmentplan_new 
                SELECT id, patient_id, checkup_id, related_disease, assigned_doctor, 
                       prescribed_medications, procedures, next_followup_date, 
                       lifestyle_recommendations, physiotherapy_advice
                FROM patients_treatmentplan
            """)
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE patients_treatmentplan")
            cursor.execute("ALTER TABLE patients_treatmentplan_new RENAME TO patients_treatmentplan")
            
            print("✅ TreatmentPlan table updated - removed NOT NULL constraints")
        
        # Also fix other tables that might have constraints
        tables_to_fix = [
            ('patients_medicalhistory', [
                'past_conditions TEXT',
                'family_history TEXT', 
                'previous_surgeries TEXT',
                'allergies TEXT'
            ]),
            ('patients_checkup', [
                'symptoms TEXT',
                'current_diagnosis TEXT',
                'date_of_checkup DATE',
                'blood_pressure VARCHAR(50)',
                'heart_rate VARCHAR(50)',
                'temperature VARCHAR(50)',
                'weight VARCHAR(50)',
                'height VARCHAR(50)',
                'bmi VARCHAR(50)',
                'physical_exam_findings TEXT'
            ]),
            ('patients_labtests', [
                'lab_results TEXT',
                'imaging TEXT',
                'other_tests TEXT'
            ]),
            ('patients_additionalnote', [
                'doctor_remarks TEXT',
                'special_warnings TEXT'
            ])
        ]
        
        for table_name, fields in tables_to_fix:
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            result = cursor.fetchone()
            
            if result and 'NOT NULL' in result[0]:
                print(f"🔄 Fixing {table_name}...")
                
                # Get all columns
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                # Create new table schema
                new_columns = []
                for col in columns:
                    col_name, col_type = col[1], col[2]
                    if col_name == 'id':
                        new_columns.append(f"{col_name} INTEGER PRIMARY KEY AUTOINCREMENT")
                    elif col_name == 'patient_id':
                        new_columns.append(f"{col_name} INTEGER NOT NULL REFERENCES patients_patient(id)")
                    else:
                        # Remove NOT NULL constraint
                        new_columns.append(f"{col_name} {col_type}")
                
                new_table_sql = f"CREATE TABLE {table_name}_new ({', '.join(new_columns)})"
                cursor.execute(new_table_sql)
                
                # Copy data
                column_names = [col[1] for col in columns]
                cursor.execute(f"""
                    INSERT INTO {table_name}_new ({', '.join(column_names)})
                    SELECT {', '.join(column_names)} FROM {table_name}
                """)
                
                # Replace table
                cursor.execute(f"DROP TABLE {table_name}")
                cursor.execute(f"ALTER TABLE {table_name}_new RENAME TO {table_name}")
                
                print(f"✅ {table_name} updated")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Database constraints fixed successfully!")
        print("📋 All tables now allow NULL values for optional fields")
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        # Restore backup
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, db_path)
            print("🔄 Database restored from backup")

if __name__ == "__main__":
    fix_database_constraints()
