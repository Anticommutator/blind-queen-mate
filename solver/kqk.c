// Blind (premove) KQK solver. usage: kqk wk q [bk]  -> without bk: test all bk, report first failure
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t U;
static U KB[64]; static int RAY[64][8][8], RLEN[64][8];
static const int DF[8]={-1,-1,-1,0,0,1,1,1}, DR[8]={-1,0,1,-1,1,-1,0,1};
static void initT(void){
  for(int s=0;s<64;s++){int f=s%8,r=s/8;KB[s]=0;
    for(int d=0;d<8;d++){int x=f+DF[d],y=r+DR[d]; if(x>=0&&x<8&&y>=0&&y<8)KB[s]|=1ULL<<(y*8+x);
      RLEN[s][d]=0; x=f+DF[d];y=r+DR[d]; while(x>=0&&x<8&&y>=0&&y<8){RAY[s][d][RLEN[s][d]++]=y*8+x;x+=DF[d];y+=DR[d];}}}
}
static U qatt(int q,int wk){U A=0;for(int d=0;d<8;d++)for(int i=0;i<RLEN[q][d];i++){int t=RAY[q][d][i];A|=1ULL<<t;if(t==wk)break;}return A;}
static U QA[64][64];
static U dil(U S){U a=0xfefefefefefefefeULL,h=0x7f7f7f7f7f7f7f7fULL;U x=S|((S<<1)&a)|((S>>1)&h);return x|(x<<8)|(x>>8);}
// hash set
#define HB 25
static U *hk; static uint16_t *hm; static uint8_t *hu; static size_t HN=1ULL<<HB;
static int hins(U S,uint16_t kq){U h=(S*0x9E3779B97F4A7C15ULL)^(kq*0xC2B2AE3D27D4EB4FULL);h^=h>>29;size_t i=h&(HN-1);
  while(hu[i]){if(hk[i]==S&&hm[i]==kq)return 0;i=(i+1)&(HN-1);}hu[i]=1;hk[i]=S;hm[i]=kq;return 1;}
// heap
typedef struct{int f;int d;uint16_t kq;U S;}E; static E*hp; static size_t hn,hcap;
static void push(E e){if(hn==hcap){hcap=hcap?hcap*2:1<<20;hp=realloc(hp,hcap*sizeof(E));}size_t i=hn++;while(i){size_t p=(i-1)/2;if(hp[p].f<=e.f)break;hp[i]=hp[p];i=p;}hp[i]=e;}
static E pop(void){E t=hp[0],l=hp[--hn];size_t i=0;for(;;){size_t c=2*i+1;if(c>=hn)break;if(c+1<hn&&hp[c+1].f<hp[c].f)c++;if(hp[c].f>=l.f)break;hp[i]=hp[c];i=c;}hp[i]=l;return t;}
static long LIMIT=50000000;
// returns mate length, -1 none (exhausted), -2 limit
static int solve(int wk,int q,U S0){
  memset(hu,0,HN);hn=0; long n=0; hins(S0,wk*64+q); push((E){0,0,wk*64+q,S0});
  while(hn){E e=pop(); if(++n>LIMIT)return -2; int k=e.kq/64,qq=e.kq%64;U S=e.S,adj=dil(S);
    int ck[64],cq[64],nc=0;
    U kb=KB[k]; while(kb){int t=__builtin_ctzll(kb);kb&=kb-1; if(t!=qq&&!((adj>>t)&1)){ck[nc]=t;cq[nc++]=qq;}}
    for(int d=0;d<8;d++)for(int i=0;i<RLEN[qq][d];i++){int t=RAY[qq][d][i];if(t==k||((S>>t)&1))break;ck[nc]=k;cq[nc++]=t;}
    for(int c=0;c<nc;c++){int nk=ck[c],nq=cq[c];
      if(!((KB[nk]>>nq)&1)&&((adj>>nq)&1))continue;
      U A=QA[nq][nk]|KB[nk]|(1ULL<<nk), fr=~A&~(1ULL<<nq), NS=0; int ok=1; U s=S;
      while(s){int b=__builtin_ctzll(s);s&=s-1;U m=KB[b]&fr;if(!m){if(!((A>>b)&1)){ok=0;break;}}NS|=m;}
      if(!ok)continue; if(!NS)return e.d+1;
      if(hins(NS,nk*64+nq))push((E){e.d+1+2*__builtin_popcountll(NS),e.d+1,nk*64+nq,NS});}
  }
  return -1;
}
static int dist(int a,int b){int x=abs(a%8-b%8),y=abs(a/8-b/8);return x>y?x:y;}
int main(int argc,char**argv){initT();for(int a=0;a<64;a++)for(int b=0;b<64;b++)QA[a][b]=qatt(a,b);
  hk=malloc(HN*8);hm=malloc(HN*2);hu=malloc(HN);
  int wk=atoi(argv[1]),q=atoi(argv[2]);
  U legal=~(QA[q][wk]|KB[wk]|(1ULL<<wk)|(1ULL<<q));
  if(argc>3&&argv[3][0]=='S'){U S=strtoull(argv[3]+1,0,16);printf("%s %d\n",argv[3],solve(wk,q,S));return 0;}
  if(argc>3){int bk=atoi(argv[3]);printf("%d %d %d %d\n",wk,q,bk,solve(wk,q,1ULL<<bk));return 0;}
  // order bk: farthest from white king first
  int ord[64],no=0; for(int dd=7;dd>=0;dd--)for(int b=0;b<64;b++)if(((legal>>b)&1)&&dist(b,wk)==dd)ord[no++]=b;
  int worst=0;
  for(int i=0;i<no;i++){int r=solve(wk,q,1ULL<<ord[i]);
    if(r<0){printf("%d %d FAIL bk=%d res=%d\n",wk,q,ord[i],r);return 0;} if(r>worst)worst=r;}
  printf("%d %d ALL n=%d maxlen=%d\n",wk,q,no,worst);return 0;}
