import React, { useState } from "react";
import { IconMessages, IconEdit, IconSearch } from "@tabler/icons-react";
import { Button } from "~/components/custom/Button";
import { ScrollArea } from "~/components/ui/scroll-area";
import { cn } from "~/lib/utils";
import { Link, Links } from "@remix-run/react";
import { useParams } from "@remix-run/react";
import { useConversations } from "~/contexts/ConversationContext";
import { useLocation } from "@remix-run/react";
import ToggleButton from "~/components/custom/Toggle";
interface LeftSideProps {
  onCreateNewChat?: () => void;
}

const LeftSide: React.FC<LeftSideProps> = ({ onCreateNewChat }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const { fetcher } = useConversations();
  const filteredConversations = fetcher.data
    ? fetcher.data?.filter((conv: any) =>
        conv.title.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];
  const location = useLocation();

  const { id } = useParams();
  
  const ConvList = ({ filteredConversations }: any) => {
    if (filteredConversations.length > 0) {
      return filteredConversations.map((conv: any) => (
        <Link
          key={conv.id}
          to={
            location.pathname.startsWith("/t") ? `/t/${conv.id}` : `/${conv.id}`
          }
        >
          <button
            key={conv.id}
            type="button"
            className={cn(
              `flex w-full bg-card rounded-md px-2 py-2 text-left text-primary text-sm group hover:bg-primary/75 hover:text-primary-foreground duration-75`,
              id && id === conv.id && "bg-primary text-primary-foreground"
            )}
          >
            <IconMessages className="mr-2" />
            {conv.title}
          </button>
        </Link>
      ));
    }
    return null;
  };

  const EmptyList = ({ filteredConversations }: any) => {
    if (filteredConversations.length == 0) {
      return (
        <div className="flex h-full w-full items-center justify-center">
          <p>No conversations</p>
        </div>
      );
    }
    return null;
  };
  return (
    <div className="flex h-full w-full flex-shrink-0 flex-col gap-2 sm:w-56 lg:w-72 2xl:w-80">
      <div className="flex w-full flex-col gap-2 bg-background px-4 pb-3 shadow-sm">
        <div className="flex items-center justify-between py-2">
          <div className="flex gap-2">
            <Link to="/">
              <h1 className="text-2xl font-bold">TSH.ai</h1>
            </Link>
            <IconMessages size={20} />
          </div>
          <Button
            size="icon"
            variant="ghost"
            className="rounded-lg"
            onClick={onCreateNewChat}
          >
            <IconEdit size={24} className="stroke-muted-foreground" />
          </Button>
        </div>
        <ToggleButton/>
        <label className="flex h-12 w-full items-center space-x-0 rounded-md border border-input pl-2 focus-within:outline-none focus-within:ring-1 focus-within:ring-ring">
          <IconSearch size={15} className="mr-2 stroke-slate-500" />
          <span className="sr-only">Search</span>
          <input
            type="text"
            className="w-full flex-1 bg-inherit text-sm focus-visible:outline-none"
            placeholder="Search chat..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </label>
      </div>

      <ScrollArea className="h-full px-4 py-2">
        <div className="flex h-full w-full flex-col gap-2">
          <ConvList filteredConversations={filteredConversations} />
          <EmptyList filteredConversations={filteredConversations} />
        </div>
      </ScrollArea>
    </div>
  );
};

export default LeftSide;
