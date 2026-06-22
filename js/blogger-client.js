const BloggerClient = {
    apiKey: null,
    accessToken: null,
    blogId: null,
    webClientId: null,
    
    init: function(options = {}) {
        this.apiKey = options.apiKey || null;
        this.blogId = options.blogId || 'G-F7ZG182KN2';
        this.accessToken = options.accessToken || null;
        this.webClientId = options.webClientId || null;
        
        if (this.webClientId && typeof google !== 'undefined' && google.accounts && google.accounts.id) {
            google.accounts.id.initialize({
                client_id: this.webClientId,
                callback: this._handleCredentialResponse.bind(this),
                scope: 'https://www.googleapis.com/auth/blogger'
            });
        }
    },
    
    _handleCredentialResponse: function(response) {
        const credential = response.credential;
        this.accessToken = credential;
        if (this.onAuthSuccess) {
            this.onAuthSuccess(credential);
        }
    },
    
    setAccessToken: function(token) {
        this.accessToken = token;
    },
    
    setApiKey: function(key) {
        this.apiKey = key;
    },
    
    setWebClientId: function(clientId) {
        this.webClientId = clientId;
    },
    
    renderAuthButton: function(element) {
        if (this.webClientId && typeof google !== 'undefined' && google.accounts && google.accounts.id) {
            google.accounts.id.renderButton(element, {
                theme: 'outline',
                text: 'signin_with',
                shape: 'circle',
                size: 'large'
            });
        }
    },
    
    buildUrl: function(endpoint, params = {}) {
        const baseUrl = `https://www.googleapis.com/blogger/v3${endpoint}`;
        const searchParams = new URLSearchParams();
        
        if (this.apiKey) {
            searchParams.append('key', this.apiKey);
        }
        
        Object.entries(params).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                searchParams.append(key, value);
            }
        });
        
        return `${baseUrl}?${searchParams.toString()}`;
    },
    
    getHeaders: function() {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (this.accessToken) {
            headers['Authorization'] = `Bearer ${this.accessToken}`;
        }
        
        return headers;
    },
    
    async getPosts(maxResults = 100) {
        const url = this.buildUrl(`/blogs/${this.blogId}/posts`, { maxResults });
        const response = await fetch(url, { headers: this.getHeaders() });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return response.json();
    },
    
    async getPost(postId) {
        const url = this.buildUrl(`/blogs/${this.blogId}/posts/${postId}`);
        const response = await fetch(url, { headers: this.getHeaders() });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return response.json();
    },
    
    async getBlog() {
        const url = this.buildUrl(`/blogs/${this.blogId}`);
        const response = await fetch(url, { headers: this.getHeaders() });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return response.json();
    }
};

window.BloggerClient = BloggerClient;