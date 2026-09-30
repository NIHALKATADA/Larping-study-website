-- PHASE 1.5 SCHEMA: LEGACY CONTENT IMPORT
-- Run this in your Supabase SQL Editor.

CREATE TABLE IF NOT EXISTS public.content_import_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_by UUID REFERENCES auth.users(id),
    started_at TIMESTAMPTZ DEFAULT now(),
    completed_at TIMESTAMPTZ,
    status TEXT,
    source_version TEXT,
    records_processed INT DEFAULT 0,
    records_failed INT DEFAULT 0,
    error_log TEXT
);

CREATE TABLE IF NOT EXISTS public.legacy_subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id TEXT NOT NULL,
    created_by UUID REFERENCES auth.users(id),
    source_type TEXT DEFAULT 'legacy-static',
    source_path TEXT,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    metadata JSONB,
    UNIQUE (subject_id, created_by)
);

CREATE TABLE IF NOT EXISTS public.legacy_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id TEXT NOT NULL,
    original_id TEXT NOT NULL,
    title TEXT,
    answer_html TEXT,
    legacy_importance NUMERIC,
    legacy_difficulty NUMERIC,
    created_by UUID REFERENCES auth.users(id),
    source_type TEXT DEFAULT 'legacy-static',
    source_path TEXT,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    metadata JSONB,
    UNIQUE (subject_id, original_id, created_by)
);

CREATE TABLE IF NOT EXISTS public.legacy_quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id TEXT NOT NULL,
    original_id TEXT NOT NULL,
    question TEXT,
    options JSONB,
    correct_answer TEXT,
    explanation TEXT,
    created_by UUID REFERENCES auth.users(id),
    source_type TEXT DEFAULT 'legacy-static',
    source_path TEXT,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    metadata JSONB,
    UNIQUE (subject_id, original_id, created_by)
);

CREATE TABLE IF NOT EXISTS public.legacy_coverage_gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id TEXT NOT NULL,
    original_id TEXT NOT NULL,
    gap_data JSONB,
    created_by UUID REFERENCES auth.users(id),
    source_type TEXT DEFAULT 'legacy-static',
    source_path TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (subject_id, original_id, created_by)
);

CREATE TABLE IF NOT EXISTS public.legacy_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    content TEXT,
    created_by UUID REFERENCES auth.users(id),
    source_type TEXT DEFAULT 'legacy-static',
    source_path TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (subject_id, resource_type, created_by)
);

-- Row Level Security setup
ALTER TABLE public.content_import_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legacy_subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legacy_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legacy_quizzes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legacy_coverage_gaps ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.legacy_resources ENABLE ROW LEVEL SECURITY;

-- Note: Legacy content is intentionally kept private to the importer during Phase 1.5.
-- 'is_published' has no effect currently without an accompanying public read policy.

-- Drop existing policies for idempotency
DROP POLICY IF EXISTS "Users can view own imports" ON public.content_import_runs;
DROP POLICY IF EXISTS "Users can insert own imports" ON public.content_import_runs;
DROP POLICY IF EXISTS "Users can update own imports" ON public.content_import_runs;

DROP POLICY IF EXISTS "Users can view own subjects" ON public.legacy_subjects;
DROP POLICY IF EXISTS "Users can insert own subjects" ON public.legacy_subjects;
DROP POLICY IF EXISTS "Users can update own subjects" ON public.legacy_subjects;
DROP POLICY IF EXISTS "Users can delete own subjects" ON public.legacy_subjects;

DROP POLICY IF EXISTS "Users can view own questions" ON public.legacy_questions;
DROP POLICY IF EXISTS "Users can insert own questions" ON public.legacy_questions;
DROP POLICY IF EXISTS "Users can update own questions" ON public.legacy_questions;
DROP POLICY IF EXISTS "Users can delete own questions" ON public.legacy_questions;

DROP POLICY IF EXISTS "Users can view own quizzes" ON public.legacy_quizzes;
DROP POLICY IF EXISTS "Users can insert own quizzes" ON public.legacy_quizzes;
DROP POLICY IF EXISTS "Users can update own quizzes" ON public.legacy_quizzes;
DROP POLICY IF EXISTS "Users can delete own quizzes" ON public.legacy_quizzes;

DROP POLICY IF EXISTS "Users can view own coverage gaps" ON public.legacy_coverage_gaps;
DROP POLICY IF EXISTS "Users can insert own coverage gaps" ON public.legacy_coverage_gaps;
DROP POLICY IF EXISTS "Users can update own coverage gaps" ON public.legacy_coverage_gaps;
DROP POLICY IF EXISTS "Users can delete own coverage gaps" ON public.legacy_coverage_gaps;

DROP POLICY IF EXISTS "Users can view own resources" ON public.legacy_resources;
DROP POLICY IF EXISTS "Users can insert own resources" ON public.legacy_resources;
DROP POLICY IF EXISTS "Users can update own resources" ON public.legacy_resources;
DROP POLICY IF EXISTS "Users can delete own resources" ON public.legacy_resources;

-- Policies for content_import_runs
CREATE POLICY "Users can view own imports" ON public.content_import_runs FOR SELECT USING (auth.uid() = started_by);
CREATE POLICY "Users can insert own imports" ON public.content_import_runs FOR INSERT WITH CHECK (auth.uid() = started_by);
CREATE POLICY "Users can update own imports" ON public.content_import_runs FOR UPDATE USING (auth.uid() = started_by);

-- Policies for legacy_subjects
CREATE POLICY "Users can view own subjects" ON public.legacy_subjects FOR SELECT USING (auth.uid() = created_by);
CREATE POLICY "Users can insert own subjects" ON public.legacy_subjects FOR INSERT WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can update own subjects" ON public.legacy_subjects FOR UPDATE USING (auth.uid() = created_by) WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can delete own subjects" ON public.legacy_subjects FOR DELETE USING (auth.uid() = created_by);

-- Policies for legacy_questions
CREATE POLICY "Users can view own questions" ON public.legacy_questions FOR SELECT USING (auth.uid() = created_by);
CREATE POLICY "Users can insert own questions" ON public.legacy_questions FOR INSERT WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can update own questions" ON public.legacy_questions FOR UPDATE USING (auth.uid() = created_by) WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can delete own questions" ON public.legacy_questions FOR DELETE USING (auth.uid() = created_by);

-- Policies for legacy_quizzes
CREATE POLICY "Users can view own quizzes" ON public.legacy_quizzes FOR SELECT USING (auth.uid() = created_by);
CREATE POLICY "Users can insert own quizzes" ON public.legacy_quizzes FOR INSERT WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can update own quizzes" ON public.legacy_quizzes FOR UPDATE USING (auth.uid() = created_by) WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can delete own quizzes" ON public.legacy_quizzes FOR DELETE USING (auth.uid() = created_by);

-- Policies for legacy_coverage_gaps
CREATE POLICY "Users can view own coverage gaps" ON public.legacy_coverage_gaps FOR SELECT USING (auth.uid() = created_by);
CREATE POLICY "Users can insert own coverage gaps" ON public.legacy_coverage_gaps FOR INSERT WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can update own coverage gaps" ON public.legacy_coverage_gaps FOR UPDATE USING (auth.uid() = created_by) WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can delete own coverage gaps" ON public.legacy_coverage_gaps FOR DELETE USING (auth.uid() = created_by);

-- Policies for legacy_resources
CREATE POLICY "Users can view own resources" ON public.legacy_resources FOR SELECT USING (auth.uid() = created_by);
CREATE POLICY "Users can insert own resources" ON public.legacy_resources FOR INSERT WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can update own resources" ON public.legacy_resources FOR UPDATE USING (auth.uid() = created_by) WITH CHECK (auth.uid() = created_by);
CREATE POLICY "Users can delete own resources" ON public.legacy_resources FOR DELETE USING (auth.uid() = created_by);

-- Explicit Data API Grants
REVOKE ALL ON TABLE public.content_import_runs FROM anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.content_import_runs TO authenticated;

REVOKE ALL ON TABLE public.legacy_subjects FROM anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.legacy_subjects TO authenticated;

REVOKE ALL ON TABLE public.legacy_questions FROM anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.legacy_questions TO authenticated;

REVOKE ALL ON TABLE public.legacy_quizzes FROM anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.legacy_quizzes TO authenticated;

REVOKE ALL ON TABLE public.legacy_coverage_gaps FROM anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.legacy_coverage_gaps TO authenticated;

REVOKE ALL ON TABLE public.legacy_resources FROM anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.legacy_resources TO authenticated;
