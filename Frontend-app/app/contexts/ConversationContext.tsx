import React, {
  createContext,
  useState,
  useContext,
  ReactNode,
  useEffect,
} from "react";
import { useFetcher, useLocation } from "@remix-run/react";
import { initialModel } from "~/lib/data/ModelOptions";

interface ConversationContextType {
  model: any;
  setModel: any;
  fetcher: ReturnType<typeof useFetcher>; // Specify the fetcher type
}

const ConversationContext = createContext<ConversationContextType | undefined>(
  undefined
);

export const ConversationProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const fetcherC = useFetcher();
  const fetcherT = useFetcher();
  const [model, setModel] = useState(initialModel);
  const location = useLocation();

  const fetcher = location.pathname.startsWith("/t")
    ? fetcherT
    : fetcherC;

    const uuid4Pattern = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/;

    useEffect(() => {
      // Check if the pathname starts with "/t/"
      if (location.pathname == "/t" || location.pathname.startsWith("/t/")) {
        fetcherT.load("/t"); // Load task data
      } 
      // Check if the pathname is "/" or matches the UUID4 pattern after the first "/"
      else if (location.pathname === '/' || uuid4Pattern.test(location.pathname.split('/')[1])) {
        fetcherC.load("/c");
      }
    }, [location.pathname]);

  return (
    <ConversationContext.Provider
      value={{
        model,
        setModel,
        fetcher,
      }}
    >
      {children}
    </ConversationContext.Provider>
  );
};

export const useConversations = () => {
  const context = useContext(ConversationContext);
  if (context === undefined) {
    throw new Error(
      "useConversations must be used within a ConversationProvider"
    );
  }
  return context;
};
