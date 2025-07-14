// Layout.tsx - Modern Block.inc inspired design

import { BottomPanel } from '@/components/panels/bottom/bottom-panel';
import { LeftSidebar } from '@/components/panels/left/left-sidebar';
import { RightSidebar } from '@/components/panels/right/right-sidebar';
import { TabBar } from '@/components/tabs/tab-bar';
import { TabContent } from '@/components/tabs/tab-content';
import { SidebarProvider } from '@/components/ui/sidebar';
import { FlowProvider, useFlowContext } from '@/contexts/flow-context';
import { TabsProvider, useTabsContext } from '@/contexts/tabs-context';
import { useLayoutKeyboardShortcuts } from '@/hooks/use-keyboard-shortcuts';
import { cn } from '@/lib/utils';
import { SidebarStorageService } from '@/services/sidebar-storage';
import { TabService } from '@/services/tab-service';
import { ReactFlowProvider } from '@xyflow/react';
import { ReactNode, useEffect, useState } from 'react';
import { TopBar } from './layout/top-bar';

// Create a LayoutContent component to access the FlowContext and TabsContext
function LayoutContent({ children }: { children: ReactNode }) {
  const { reactFlowInstance } = useFlowContext();
  const { openTab } = useTabsContext();
  
  // Initialize sidebar states from storage service
  const [isLeftCollapsed, setIsLeftCollapsed] = useState(() => 
    SidebarStorageService.loadLeftSidebarState(true)
  );
  
  const [isRightCollapsed, setIsRightCollapsed] = useState(() => 
    SidebarStorageService.loadRightSidebarState(true)
  );

  const [isBottomCollapsed, setIsBottomCollapsed] = useState(() => 
    SidebarStorageService.loadBottomPanelState(true)
  );

  // Track actual sidebar widths for dynamic positioning
  const [leftSidebarWidth, setLeftSidebarWidth] = useState(280);
  const [rightSidebarWidth, setRightSidebarWidth] = useState(280);
  const [bottomPanelHeight, setBottomPanelHeight] = useState(300);

  const handleSettingsClick = () => {
    const tabData = TabService.createSettingsTab();
    openTab(tabData);
  };

  // Add keyboard shortcuts for toggling sidebars and fit view
  useLayoutKeyboardShortcuts(
    () => setIsRightCollapsed(!isRightCollapsed), // Cmd+I for right sidebar
    () => setIsLeftCollapsed(!isLeftCollapsed),   // Cmd+B for left sidebar
    () => reactFlowInstance.fitView({ padding: 0.1, duration: 500 }), // Cmd+O for fit view
    // Note: undo/redo will be handled directly in the Flow component for now
    undefined, // undo
    undefined, // redo
    () => setIsBottomCollapsed(!isBottomCollapsed), // Cmd+J for bottom panel
    handleSettingsClick, // Shift+Cmd+J for settings
  );

  // Save sidebar states whenever they change
  useEffect(() => {
    SidebarStorageService.saveLeftSidebarState(isLeftCollapsed);
  }, [isLeftCollapsed]);

  useEffect(() => {
    SidebarStorageService.saveRightSidebarState(isRightCollapsed);
  }, [isRightCollapsed]);

  useEffect(() => {
    SidebarStorageService.saveBottomPanelState(isBottomCollapsed);
  }, [isBottomCollapsed]);

  // Calculate tab bar and bottom panel positioning based on actual sidebar widths
  const getSidebarBasedStyle = () => {
    let left = 0;
    let right = 0;
    
    if (!isLeftCollapsed) {
      left = leftSidebarWidth;
    }
    
    if (!isRightCollapsed) {
      right = rightSidebarWidth;
    }
    
    return {
      left: `${left}px`,
      right: `${right}px`,
    };
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden relative bg-background">
      {/* Modern VSCode-style Top Bar */}
      <TopBar
        isLeftCollapsed={isLeftCollapsed}
        isRightCollapsed={isRightCollapsed}
        isBottomCollapsed={isBottomCollapsed}
        onToggleLeft={() => setIsLeftCollapsed(!isLeftCollapsed)}
        onToggleRight={() => setIsRightCollapsed(!isRightCollapsed)}
        onToggleBottom={() => setIsBottomCollapsed(!isBottomCollapsed)}
        onSettingsClick={handleSettingsClick}
      />

      {/* Modern Tab Bar with glass effect */}
      <div 
        className="absolute top-0 z-20 panel-transition glass-panel"
        style={getSidebarBasedStyle()}
      >
        <TabBar />
      </div>

      {/* Main content area with modern styling */}
      <main 
        className="absolute inset-0 overflow-hidden bg-background panel-transition" 
        style={{
          left: !isLeftCollapsed ? `${leftSidebarWidth}px` : '0px',
          right: !isRightCollapsed ? `${rightSidebarWidth}px` : '0px',
          top: '48px', // Slightly larger tab bar for modern look
          bottom: !isBottomCollapsed ? `${bottomPanelHeight}px` : '0px',
        }}
      >
        <TabContent className="h-full w-full" />
      </main>

      {/* Modern floating left sidebar with elevation */}
      <div className={cn(
        "absolute top-0 left-0 z-30 h-full panel-transition",
        isLeftCollapsed && "transform -translate-x-full opacity-0"
      )}>
        <LeftSidebar
          isCollapsed={isLeftCollapsed}
          onCollapse={() => setIsLeftCollapsed(true)}
          onExpand={() => setIsLeftCollapsed(false)}
          onToggleCollapse={() => setIsLeftCollapsed(!isLeftCollapsed)}
          onWidthChange={setLeftSidebarWidth}
        />
      </div>

      {/* Modern floating right sidebar with elevation */}
      <div className={cn(
        "absolute top-0 right-0 z-30 h-full panel-transition",
        isRightCollapsed && "transform translate-x-full opacity-0"
      )}>
        <RightSidebar
          isCollapsed={isRightCollapsed}
          onCollapse={() => setIsRightCollapsed(true)}
          onExpand={() => setIsRightCollapsed(false)}
          onToggleCollapse={() => setIsRightCollapsed(!isRightCollapsed)}
          onWidthChange={setRightSidebarWidth}
        />
      </div>

      {/* Modern bottom panel with glass effect */}
      <div 
        className={cn(
          "absolute bottom-0 z-20 panel-transition",
          isBottomCollapsed && "transform translate-y-full opacity-0"
        )}
        style={getSidebarBasedStyle()}
      >
        <BottomPanel
          isCollapsed={isBottomCollapsed}
          onCollapse={() => setIsBottomCollapsed(true)}
          onExpand={() => setIsBottomCollapsed(false)}
          onToggleCollapse={() => setIsBottomCollapsed(!isBottomCollapsed)}
          onHeightChange={setBottomPanelHeight}
        />
      </div>
    </div>
  );
}

type LayoutProps = {
  children?: ReactNode;
};

export function Layout({ children }: LayoutProps) {
  return (
    <SidebarProvider defaultOpen={true}>
      <ReactFlowProvider>
        <FlowProvider>
          <TabsProvider>
            <LayoutContent>{children}</LayoutContent>
          </TabsProvider>
        </FlowProvider>
      </ReactFlowProvider>
    </SidebarProvider>
  );
}