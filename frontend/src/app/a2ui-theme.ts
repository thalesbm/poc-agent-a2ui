import { Theme } from '@a2ui/angular';

export const a2uiTheme: Theme = {
  components: {
    AudioPlayer: {},
    Button: {},
    Card: {},
    Column: {},
    CheckBox: {
      container: {},
      element: {},
      label: {}
    },
    DateTimeInput: {
      container: {},
      element: {},
      label: {}
    },
    Divider: {},
    Image: {
      all: {},
      icon: {},
      avatar: {},
      smallFeature: {},
      mediumFeature: {},
      largeFeature: {},
      header: {}
    },
    Icon: {},
    List: {},
    Modal: {
      backdrop: {},
      element: {}
    },
    MultipleChoice: {
      container: {},
      element: {},
      label: {}
    },
    Row: {},
    Slider: {
      container: {},
      element: {},
      label: {}
    },
    Tabs: {
      container: {},
      element: {},
      controls: {
        all: {},
        selected: {}
      }
    },
    Text: {
      all: {},
      h1: {},
      h2: {},
      h3: {},
      h4: {},
      h5: {},
      caption: {},
      body: {}
    },
    TextField: {
      container: {},
      element: {},
      label: {}
    },
    Video: {}
  },
  elements: {
    a: {},
    audio: {},
    body: {},
    button: {},
    h1: {},
    h2: {},
    h3: {},
    h4: {},
    h5: {},
    iframe: {},
    input: {},
    p: {},
    pre: {},
    textarea: {},
    video: {}
  },
  markdown: {
    p: [],
    h1: [],
    h2: [],
    h3: [],
    h4: [],
    h5: [],
    ul: [],
    ol: [],
    li: [],
    a: [],
    strong: [],
    em: []
  },
  additionalStyles: {
    Card: {
      'background': '#ffffff',
      'border-radius': '8px',
      'padding': '20px',
      'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
      'transition': 'all 0.3s ease',
      'border': '1px solid #e0e0e0',
      'position': 'relative',
      'margin-bottom': '16px',
    },
    List: {
      'display': 'flex',
      'flex-direction': 'column',
      'gap': '16px',
    },
    Row: {
      'display': 'flex',
      'flex-direction': 'row',
      'align-items': 'center',
      'gap': '12px',
    },
    Column: {
      'display': 'flex',
      'flex-direction': 'column',
      'gap': '12px',
    },
    Text: {
      'margin': '0',
      'padding': '0',
    }
  }
};

