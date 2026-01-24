export const mockLogin = (username: string, password: string) => {
  // super simple mock
  return username === "admin" && password === "admin123";
};
