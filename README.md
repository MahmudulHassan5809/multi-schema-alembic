
## 🛠️ Alembic Migration Commands

### Blog: https://www.linkedin.com/pulse/complete-guide-multi-tenant-postgresql-schema-using-alembic-hassan-aeync

### 🔄 Reset Database

Drop and recreate the entire database.

```bash
python cli.py reset-db
```

---

### 🧹 Reset Migrations

Delete all existing migration files from both public and tenant folders.

```bash
python cli.py reset-migrations
```

---

### 📦 Create Public Migration

Generate a new migration file for the **public** schema.

```bash
python cli.py revision-public -m "Your migration message"
```

---

### 🏢 Create Tenant Migration

Generate a new migration file for **tenant schemas**.

```bash
python cli.py revision -m "Your migration message"
```

---

### 🚀 Apply Public Migrations

Run all unapplied migrations for the **public** schema.

```bash
python cli.py upgrade-public
```

---

### 🚀 Apply Tenant Migrations

Run all unapplied migrations for a specific **tenant schema**.

```bash
python cli.py upgrade your_tenant_name
```
