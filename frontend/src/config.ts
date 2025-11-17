const getApiUrl = (): string => {
  if (import.meta.env.DEV) {
    return "http://localhost:8000";
  }

  const hostName = window.location.hostname;

  if (hostName === "localhost" || hostName === "127.0.0.1") {
    return "http://localhost:8000";
  }

  return `https://${hostName}:8000`;
};

export const API_URL = getApiUrl();
