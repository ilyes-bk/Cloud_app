import { Copy, CheckCheck, XCircle } from "lucide-react";
import React from "react";

const ResponseIndicator = React.memo(({ value }: any) => {
  if (value == "") {
    return (
      <>
        <XCircle size={14} color="red" />
        <span className="ml-1 text-sm">Fail</span>
      </>
    );
  } else if (!value) {
    return <span className="ml-1 text-sm">Processing</span>;
  } else {
    return (
      <>
        <CheckCheck
          size={14}
          className="stroke-current text-green-500 fill-transparent"
        />
        <span className="ml-1 text-sm ">Success</span>
      </>
    );
  }
});

// Memoize the ToolCall component to avoid unnecessary re-renders
const ToolCall = React.memo(
  ({ call, messages, indexIsLast, lastMessageRef }: any) => {
    const response = messages.find(
      (message: any) =>
        message.type == "tool" && call.id == message.tool_call_id
    )?.content;

    return (
      <>
        <div
          ref={indexIsLast ? lastMessageRef : null}
          className="flex items-start all-unset justify-start mr-8"
        ></div>
        <div className="inline-block px-4 py-2 rounded-lg bg-secondary text-secondary-foreground prose">
          <strong>{callMap(call.name, call.args)}</strong>
          <div className="flex items-center">
            <ResponseIndicator value={response} />
          </div>
        </div>
      </>
    );
  }
);

const callMap = (callName: string, args: any) => {
  if (callName == "find_order_information") {
    return `Searching Order ${args?.order_number || "Unexpected call"}`;
  } else if (callName == "get_email_threads") {
    return `Searching Email Threads: ${args?.email || "Unexpected call"}`;
  } else if (callName == "get_email_threads_by_subject") {
    return `Searching Email Threads with Subject ${
      args?.subject || "Unexpected call"
    }`;
  } else if (callName == "get_product_information") {
    return `Searching Product Pages: ${args?.keywords || "Unexpected call"}`;
  } else if (callName == "get_information_from_manual") {
    return `Searching Manuals: ${args?.query || "Unexpected call"}`;
  } else if (callName == "get_product_metadata_information") {
    return `Searching Product Information: ${
      args?.keywords || "Unexpected call"
    }`;
  } else if (callName == "get_draft_information") {
    return `Searching Draft: ${args?.order_number || "Unexpected call"}`;
  } else if (callName == "use_style") {
    return `Using Style: ${args?.style || "Unexpected call"}`;
  } else if (callName == "get_phone_conversation") {
    return `Searching Call: ${args?.number || "Unexpected call"}`;
  } else if (callName == "create_draft_order") {
    return `Creating Draft Order: ${args?.email || "Unexpected call"}`;
  } else if (callName == "add_customer_to_crm") {
    return `Adding Customer to CRM: ${
      args?.customer_name || "Unexpected call"
    }`;
  } else if (callName == "find_email_threads_with_order") {
    return `Searching threads from event comments Order`;
  } else {
    return "Unknown Tool Call";
  }
};

export default ToolCall;
