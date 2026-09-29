import { signUp, signIn, signOut, getCurrentUser, onAuthStateChange } from './auth.js';
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
        } else if (mode === 'signup') {
            authModalTitle.textContent = 'Sign Up';
            displayNameGroup.style.display = 'flex';
            passwordGroup.style.display = 'flex';
            authPassword.required = true;
            authSubmitBtn.textContent = 'Sign Up';
            authToggleMode.textContent = "Already have an account? Log In";
            authToggleMode.style.display = 'block';
            authForgotPassword.style.display = 'none';
        } else if (mode === 'reset') {
            authModalTitle.textContent = 'Reset Password';
            displayNameGroup.style.display = 'none';
            passwordGroup.style.display = 'none';
            authPassword.required = false;
            authSubmitBtn.textContent = 'Send Reset Email';
            authToggleMode.textContent = "Back to Log In";
            authToggleMode.style.display = 'block';
            authForgotPassword.style.display = 'none';
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
