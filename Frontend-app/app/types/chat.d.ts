interface ToolCall {
  args: any;
  id: string;
  name: string;
  type: string;
}

export interface Message {
  additional_kwargs: object[];
  content: string;
  example: boolean;
  id: string;
  invalid_tool_calls: object[];
  name: null | string;
  tool_calls: ToolCall[];
  type: 'ai' | 'human' | 'tool';
  usage_metadata: any;
} 

// ToolCall and Message Interfaces are effectively Langchain interfaces

export interface Conversation {
  id: string;
  title?: string;
  messages: Message[];
  confirmation?: string | undefined;
}
