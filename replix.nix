{ pkgs }: {
  deps = [
    pkgs.nodejs-16_x
    pkgs.yarn
    pkgs.nodePackages.vite
    pkgs.esbuild
  ];
}