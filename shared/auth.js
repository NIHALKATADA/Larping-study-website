import { supabase } from "./supabase-client.js";

export async function signUp(email, password, displayName = "") {
    return await supabase.auth.signUp({
        email,
        password,
        options: {
            data: {
                display_name: displayName
            }
        }
    });
}

export async function signIn(email, password) {
    return await supabase.auth.signInWithPassword({
        email,
        password
    });
}

export async function signInWithGoogle() {
    return await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
            redirectTo: window.location.origin
        }
    });
}

export async function signOut() {
    return await supabase.auth.signOut();
}

export async function getCurrentUser() {
    const { data, error } = await supabase.auth.getUser();
    return {
        user: data?.user ?? null,
        error
    };
}

export function onAuthStateChange(callback) {
    return supabase.auth.onAuthStateChange(callback);
}