-- PHASE 1: USER PROFILE SCHEMA (MIGRATION)
-- Safely migrates the existing public.profiles table.
-- Run this in your Supabase SQL Editor.

-- 1. Add missing columns safely (idempotent)
ALTER TABLE public.profiles 
    ADD COLUMN IF NOT EXISTS avatar_url TEXT,
    ADD COLUMN IF NOT EXISTS university_id UUID,
    ADD COLUMN IF NOT EXISTS program_id UUID,
    ADD COLUMN IF NOT EXISTS current_semester INTEGER;

-- 2. Ensure RLS is enabled
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- 3. Safely reconcile existing RLS policies
-- Drop the original existing policies to prevent conflicts and duplicates
DROP POLICY IF EXISTS "Users can view own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can delete own profile" ON public.profiles;

-- Create exactly one final policy for each operation using the expected names
CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING ( auth.uid() = id );

CREATE POLICY "Users can insert own profile"
    ON public.profiles FOR INSERT
    WITH CHECK ( auth.uid() = id );

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING ( auth.uid() = id )
    WITH CHECK ( auth.uid() = id );

CREATE POLICY "Users can delete own profile"
    ON public.profiles FOR DELETE
    USING ( auth.uid() = id );

-- 4. Preserve existing updated_at behavior
-- Clean up any mistakenly named triggers from earlier drafts if they were run
DROP TRIGGER IF EXISTS on_profiles_updated ON public.profiles;

-- Safely recreate the existing trigger and function to ensure one clean mechanism remains
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS profiles_set_updated_at ON public.profiles;
CREATE TRIGGER profiles_set_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW
    EXECUTE PROCEDURE public.set_updated_at();
