import { defineConfig } from 'vite';
import {pruneReleaseExports} from './scripts/release-export.mjs';
import {resolve} from 'node:path';
export default defineConfig({base:'/ruby-village/',plugins:[{
 name:'release-resources',apply:'build',
 writeBundle(options){const report=pruneReleaseExports(process.cwd(),resolve(options.dir??'dist'));console.log(`Release exports: ${(report.keptBytes/1048576).toFixed(1)} MiB; ${(report.removedBytes/1048576).toFixed(1)} MiB of archived candidates excluded`);},
}]});
