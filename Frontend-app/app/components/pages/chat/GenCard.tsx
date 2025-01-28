import { Avatar, AvatarImage, AvatarFallback } from "~/components/ui/avatar";
import ReactMarkdown from "react-markdown";
import React from "react";
interface ChatCardProps {
  message: string;
  generating: boolean;
}
const AIURL = "./logo.png";
const MessageAvatar = React.memo(({ url }: { url: string }) => {
  return (
    <Avatar>
      <AvatarImage src={url} alt="user-avatar" />
      <AvatarFallback>AI</AvatarFallback>
    </Avatar>
  );
});
<img
  src="/thinking.gif"
  alt="Thinking animation"
  style={{ width: "50px", height: "50px" }}
/>;
const GenCard: React.FC<ChatCardProps> = ({ message, generating }) => {
  if (!generating) return null;
  return message == "" ? (
    <div className={"flex items-start all-unset justify-start mr-8"}>
        <img className="mx-auto w-[300px]" src="/star.gif" />
    </div>
  ) : (
    <div className={"flex items-start all-unset justify-start mr-8"}>
      <MessageAvatar url={AIURL} />
      <div
        className={
          "inline-block px-4 py-2 rounded-lg max-w-5xl bg-secondary text-secondary-foreground relative pr-6 prose"
        }
      >
        <ReactMarkdown>{message}</ReactMarkdown>
      </div>
    </div>
  );
};

export default GenCard;
