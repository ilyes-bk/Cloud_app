import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";
/*
interface AuthContextType {
  isLoggedIn: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  checkLoginStatus: () => Promise<void>;
}
*/
interface AuthContextType {
  user: any;
  isLoggedIn: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({
  children,
  user,
}: {
  children: ReactNode;
  user: any;
}) => {
  const [isLoggedIn, setLoggedIn] = useState(false);
  useEffect(() => {
    if (user != null) {
      setLoggedIn(true);
    }
  }, []);
  /*
  const logout = () => {
    setLoggedIn(false); // Clear login state
  };
*/

  return (
    <AuthContext.Provider
      //value={{ isLoggedIn: loggedIn, login, checkLoginStatus, logout }}
      value={{ user, isLoggedIn }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
