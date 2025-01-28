import * as React from "react";
import { cn } from "~/lib/utils";
import { useEffect } from "react";
export interface InputProps
  extends React.InputHTMLAttributes<HTMLTextAreaElement> {}

const useAutosizeTextArea = (
  textAreaRef: HTMLTextAreaElement | null,
  value: string
) => {
  useEffect(() => {
    if (textAreaRef) {
      textAreaRef.style.height = "0px";
      const scrollHeight = textAreaRef.scrollHeight;
      textAreaRef.style.height = scrollHeight + "px";
    }
  }, [textAreaRef, value]);
};

const Input = React.forwardRef<HTMLTextAreaElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <textarea
        draggable="false"
        className={cn(
          "overflow-hidden resize-none text-md flex w-full rounded-md border border-input bg-transparent px-5 py-2 shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 max-h-[5rem] overflow-y-auto scrollbar-hide",
          className
        )}
        rows={1}
        ref={ref}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";

export { Input, useAutosizeTextArea };
