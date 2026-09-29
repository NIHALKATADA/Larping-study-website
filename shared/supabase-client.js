import { createClient } from "https://esm.sh/@supabase/supabase-js@2.117.2";

const response = await fetch("/api/config", {
    method: "GET",
    cache: "no-store"
});

if (!response.ok) {
    throw new Error("Unable to load Supabase configuration.");
}

const config = await response.json();

if (!config.supabaseUrl || !config.supabasePublishableKey) {
    throw new Error("Supabase configuration is incomplete.");
}

export const supabase = createClient(
    config.supabaseUrl,
    config.supabasePublishableKey,
    {
        auth: {
            autoRefreshToken: true,
            persistSession: true,
            detectSessionInUrl: true
        }
    }
);