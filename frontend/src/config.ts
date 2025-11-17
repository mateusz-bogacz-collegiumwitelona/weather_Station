const getApiUrl = (): string => {
  const hostName = window.location.hostname;

  if (hostName === "localhost" || hostName === "127.0.0.1") {
    return "http://localhost:8000";
  }

  return `http://${hostName}:8000`;
};

export const API_URL = getApiUrl();
