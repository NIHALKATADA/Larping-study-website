import { signUp, signIn, signInWithGoogle, signOut, getCurrentUser, onAuthStateChange } from './auth.js';
import { supabase } from './supabase-client.js';

export async function initAuthUI() {
    const topbar = document.querySelector('.smart-topbar');
    if (!topbar) return;

    let rightContainer = topbar.querySelector('.topbar-right');
    if (!rightContainer) {
        rightContainer = document.createElement('div');
        rightContainer.className = 'topbar-right';
        topbar.appendChild(rightContainer);
    }

    // Don't add multiple times
    if (document.getElementById('auth-ui-container')) return;

    const authContainer = document.createElement('div');
    authContainer.id = 'auth-ui-container';
    authContainer.style.display = 'flex';
    authContainer.style.alignItems = 'center';
    authContainer.style.gap = '10px';
    rightContainer.appendChild(authContainer);

    // Create Modal HTML (hidden by default)
    const modalHTML = `
    <div id="authModal" class="glass-modal" style="z-index: 100000; display: none;">
        <div class="modal-content" style="max-width: 400px; padding: 2rem;">
            <div class="modal-header" style="border: none; padding-bottom: 0;">
                <h3 id="authModalTitle" style="margin: 0; font-size: 1.5rem;">Log In</h3>
                <button class="close-modal" id="authModalClose" style="background: none; border: none; color: white; cursor: pointer; font-size: 1.5rem;">&times;</button>
            </div>
            <div class="modal-body" style="padding-top: 1rem;">
                <div id="authError" style="color: #ef4444; margin-bottom: 1rem; font-size: 0.9rem; display: none; padding: 0.5rem; background: rgba(239, 68, 68, 0.1); border-radius: 4px; border: 1px solid rgba(239, 68, 68, 0.2);"></div>
                <div id="authSuccess" style="color: #10b981; margin-bottom: 1rem; font-size: 0.9rem; display: none; padding: 0.5rem; background: rgba(16, 185, 129, 0.1); border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.2);"></div>
                
                <form id="authForm" style="display: flex; flex-direction: column; gap: 1rem;">
                    <div id="displayNameGroup" style="display: none; flex-direction: column; gap: 0.5rem;">
                        <label style="font-size: 0.9rem; color: #a0a0a5;">Display Name</label>
                        <input type="text" id="authName" class="search-bar" style="width: 100%; border-radius: 8px;" placeholder="Optional">
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <label style="font-size: 0.9rem; color: #a0a0a5;">Email</label>
                        <input type="email" id="authEmail" class="search-bar" style="width: 100%; border-radius: 8px;" required>
                    </div>
                    <div id="passwordGroup" style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <label style="font-size: 0.9rem; color: #a0a0a5;">Password</label>
                        <input type="password" id="authPassword" class="search-bar" style="width: 100%; border-radius: 8px;" required>
                    </div>
                    <button type="submit" id="authSubmitBtn" class="btn btn-primary" style="margin-top: 0.5rem;">Log In</button>
                </form>

                <div id="googleAuthSection" style="margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem;">
                    <button type="button" id="authGoogleBtn" class="btn btn-secondary" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                        Continue with Google
                    </button>
                </div>
                
                <div style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; text-align: center; font-size: 0.9rem;">
                    <a href="#" id="authToggleMode" style="color: var(--primary-teal); text-decoration: none;">Don't have an account? Sign Up</a>
                    <a href="#" id="authForgotPassword" style="color: var(--primary-teal); text-decoration: none;">Forgot Password?</a>
                </div>
            </div>
        </div>
    </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);

    let authMode = 'login'; // 'login', 'signup', 'reset'

    const authModal = document.getElementById('authModal');
    const authModalTitle = document.getElementById('authModalTitle');
    const authForm = document.getElementById('authForm');
    const displayNameGroup = document.getElementById('displayNameGroup');
    const passwordGroup = document.getElementById('passwordGroup');
    const authPassword = document.getElementById('authPassword');
    const authSubmitBtn = document.getElementById('authSubmitBtn');
    const authToggleMode = document.getElementById('authToggleMode');
    const authForgotPassword = document.getElementById('authForgotPassword');
    const authError = document.getElementById('authError');
    const authSuccess = document.getElementById('authSuccess');
    const googleAuthSection = document.getElementById('googleAuthSection');
    const authGoogleBtn = document.getElementById('authGoogleBtn');

    function showModal(mode = 'login') {
        authMode = mode;
        authError.style.display = 'none';
        authSuccess.style.display = 'none';
        authForm.reset();
        
        if (mode === 'login') {
            authModalTitle.textContent = 'Log In';
            displayNameGroup.style.display = 'none';
            passwordGroup.style.display = 'flex';
            authPassword.required = true;
            authSubmitBtn.textContent = 'Log In';
            authToggleMode.textContent = "Don't have an account? Sign Up";
            authToggleMode.style.display = 'block';
            authForgotPassword.style.display = 'block';
            googleAuthSection.style.display = 'block';
        } else if (mode === 'signup') {
            authModalTitle.textContent = 'Sign Up';
            displayNameGroup.style.display = 'flex';
            passwordGroup.style.display = 'flex';
            authPassword.required = true;
            authSubmitBtn.textContent = 'Sign Up';
            authToggleMode.textContent = "Already have an account? Log In";
            authToggleMode.style.display = 'block';
            authForgotPassword.style.display = 'none';
            googleAuthSection.style.display = 'block';
        } else if (mode === 'reset') {
            authModalTitle.textContent = 'Reset Password';
            displayNameGroup.style.display = 'none';
            passwordGroup.style.display = 'none';
            authPassword.required = false;
            authSubmitBtn.textContent = 'Send Reset Email';
            authToggleMode.textContent = "Back to Log In";
            authToggleMode.style.display = 'block';
            authForgotPassword.style.display = 'none';
            googleAuthSection.style.display = 'none';
        }

        authModal.style.display = 'flex';
        // Use a small timeout to allow display: flex to apply before adding class for animation
        setTimeout(() => {
            authModal.classList.add('active');
        }, 10);
    }

    document.getElementById('authModalClose').onclick = () => {
        authModal.classList.remove('active');
        setTimeout(() => {
            authModal.style.display = 'none';
        }, 300); // Matches typical transition time
    };

    authToggleMode.onclick = (e) => {
        e.preventDefault();
        if (authMode === 'login') showModal('signup');
        else showModal('login');
    };

    authForgotPassword.onclick = (e) => {
        e.preventDefault();
        showModal('reset');
    };

    authGoogleBtn.onclick = async () => {
        authError.style.display = 'none';
        authGoogleBtn.disabled = true;
        authGoogleBtn.style.opacity = '0.7';
        authGoogleBtn.innerHTML = '<span style="display:inline-block; animation: spin 1s linear infinite;">↻</span> Redirecting...';
        
        try {
            const { error } = await signInWithGoogle();
            if (error) throw error;
        } catch (err) {
            authError.textContent = err.message || "An error occurred with Google Sign-In.";
            authError.style.display = 'block';
            authGoogleBtn.disabled = false;
            authGoogleBtn.style.opacity = '1';
            authGoogleBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg> Continue with Google';
        }
    };

    authForm.onsubmit = async (e) => {
        e.preventDefault();
        authError.style.display = 'none';
        authSuccess.style.display = 'none';
        authSubmitBtn.disabled = true;
        authSubmitBtn.style.opacity = '0.7';

        const email = document.getElementById('authEmail').value;
        const password = authPassword.value;
        const displayName = document.getElementById('authName').value;

        try {
            if (authMode === 'login') {
                const { error } = await signIn(email, password);
                if (error) {
                    if (error.message.includes('Email not confirmed')) {
                         throw new Error('Please confirm your email address before logging in.');
                    }
                    throw error;
                }
                
                authModal.classList.remove('active');
                setTimeout(() => { authModal.style.display = 'none'; }, 300);
            } else if (authMode === 'signup') {
                const { data, error } = await signUp(email, password, displayName);
                if (error) throw error;
                
                if (data.user && data.user.identities && data.user.identities.length === 0) {
                     throw new Error("This email is already in use.");
                }
                
                authSuccess.textContent = "Success! Please check your email to confirm your account.";
                authSuccess.style.display = 'block';
                
                setTimeout(() => { 
                    if(authModal.style.display === 'flex') showModal('login'); 
                }, 4000);
            } else if (authMode === 'reset') {
                const { error } = await supabase.auth.resetPasswordForEmail(email, {
                    redirectTo: window.location.origin + '/reset-password.html'
                });
                if (error) throw error;
                authSuccess.textContent = "Reset link sent! Please check your email.";
                authSuccess.style.display = 'block';
            }
        } catch (err) {
            authError.textContent = err.message || "An error occurred. Please try again.";
            authError.style.display = 'block';
        } finally {
            authSubmitBtn.disabled = false;
            authSubmitBtn.style.opacity = '1';
        }
    };

    function renderUI(user) {
        if (user) {
            const name = user.user_metadata?.display_name || user.email.split('@')[0];
        
            authContainer.innerHTML = `
                <div style="font-size: 0.9rem; color: #a0a0a5;" class="user-indicator">
                    Hi, <strong style="color: white;"></strong>
                </div>
                <button id="authLogoutBtn" class="btn btn-secondary" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;">Log Out</button>
            `;
        
            authContainer.querySelector('.user-indicator strong').textContent = name;
        
            document.getElementById('authLogoutBtn').onclick = async () => {
                await signOut();
            };
        } else {
            authContainer.innerHTML = `
                <div style="font-size: 0.9rem; color: #a0a0a5;" class="user-indicator">Guest</div>
                <button id="authLoginBtn" class="btn btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.9rem;">Log In</button>
            `;
            document.getElementById('authLoginBtn').onclick = () => showModal('login');
        }
    }

    // Initialize state
    try {
        const { user } = await getCurrentUser();
        renderUI(user);
    } catch (e) {
        console.error("Auth init error:", e);
        renderUI(null);
    }

    // Listen for changes
    onAuthStateChange((event, session) => {
        renderUI(session?.user || null);
    });
}
