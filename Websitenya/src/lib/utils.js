import { clsx, } from "clsx";
import { twMerge } from "tailwind-merge";
import { dev } from '$app/environment';

export function cn(...inputs) {
	return twMerge(clsx(inputs));
}

const PHP_PORT = 4848; // Based on 4848.port.txt

export const getPhpBackendBaseUrl = () => {
    if (dev) {
        return `http://localhost:${PHP_PORT}`;
    }
    // In production, the PHP backend is at the root of the SvelteKit app
    return ''; // Relative path to root (empty string means relative to current domain/root)
};

// Function to generate a random idempotency key
export const generateIdempotencyKey = () => {
    return 'idemp-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
};

// Function to get the selected group ID from localStorage
export const getSelectedGroupId = () => {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('selectedGrupId');
    }
    return null;
};

// Function to get the list of groups from localStorage
export const getGroupsFromLocalStorage = () => {
    if (typeof window !== 'undefined') {
        const groupsStr = localStorage.getItem('grup');
        if (groupsStr) {
            try {
                return JSON.parse(groupsStr);
            } catch (error) {
                console.error('Error parsing groups from localStorage:', error);
                return [];
            }
        }
    }
    return [];
};

/**
 * Check if the user is authenticated as an admin
 */
export const isAdminAuthenticated = () => {
    if (typeof window !== 'undefined') {
        const adminToken = localStorage.getItem('tokenAdmin');
        return !!adminToken; // Returns true if token exists, false otherwise
    }
    return false;
};

/**
 * Check if the user is authenticated as a super admin
 */
export const isSuperAdminAuthenticated = () => {
    if (typeof window !== 'undefined') {
        const superToken = localStorage.getItem('tokenSuper');
        return !!superToken; // Returns true if token exists, false otherwise
    }
    return false;
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any