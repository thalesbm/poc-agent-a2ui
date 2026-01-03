export interface A2UIMessage {
  beginRendering?: BeginRendering;
  surfaceUpdate?: SurfaceUpdate;
  dataModelUpdate?: DataModelUpdate;
}

export interface BeginRendering {
  surfaceId: string;
  root: string;
  styles?: {
    primaryColor?: string;
    font?: string;
  };
}

export interface SurfaceUpdate {
  surfaceId: string;
  components: Component[];
}

export interface Component {
  id: string;
  weight?: number;
  component: ComponentDefinition;
}

export interface ComponentDefinition {
  Column?: ColumnComponent;
  Row?: RowComponent;
  Text?: TextComponent;
  Card?: CardComponent;
  List?: ListComponent;
  Button?: ButtonComponent;
}

export interface ColumnComponent {
  children: Children;
}

export interface RowComponent {
  children: Children;
}

export interface TextComponent {
  usageHint?: string;
  text?: TextValue;
  style?: {
    color?: string;
  };
}

export interface CardComponent {
  child: string;
}

export interface ListComponent {
  direction: string;
  children: {
    template?: {
      componentId: string;
      dataBinding: string;
    };
  };
}

export interface ButtonComponent {
  child: string;
  primary?: boolean;
  action?: {
    name: string;
    context: Array<{
      key: string;
      value: {
        path: string;
      };
    }>;
  };
}

export interface Children {
  explicitList?: string[];
  template?: {
    componentId: string;
    dataBinding: string;
  };
}

export interface TextValue {
  path?: string;
  literalString?: string;
  format?: string;
}

export interface DataModelUpdate {
  surfaceId: string;
  path: string;
  contents: Content[];
}

export interface Content {
  key: string;
  valueString?: string;
  valueNumber?: number;
  valueMap?: Content[];
}

// Stock Model
export interface Stock {
  symbol: string;
  company: string;
  sector: string;
  currentPrice: number;
  recommendation: string;
  targetPrice: number;
}

