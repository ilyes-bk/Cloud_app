import { Avatar, AvatarImage, AvatarFallback } from "~/components/ui/avatar";
import ReactMarkdown from "react-markdown";
import React from "react";
import remarkBreaks from "remark-breaks";
interface ChatCardProps {
  confirmation: string | undefined;
}
const AIURL = "/logo.png";
const MessageAvatar = React.memo(({ url }: { url: string }) => {
  return (
    <Avatar>
      <AvatarImage src={url} alt="user-avatar" />
      <AvatarFallback>AI</AvatarFallback>
    </Avatar>
  );
});
const ConfirmationCard: React.FC<ChatCardProps> = ({ confirmation }) => {
  if (!confirmation) return null;
  return (
    <div className={"flex items-start all-unset justify-start mr-8"}>
      <MessageAvatar url={AIURL} />
      <div className="inline-block px-4 py-2 rounded-lg max-w-5xl bg-secondary text-secondary-foreground relative pr-6 prose">
        <ReactMarkdown remarkPlugins={[remarkBreaks]}>
          {confirmation}
        </ReactMarkdown>
      </div>
    </div>
  );
};

export default ConfirmationCard;
