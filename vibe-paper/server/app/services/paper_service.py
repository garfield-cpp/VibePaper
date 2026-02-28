from typing import List, Optional
from app.models.paper import Paper
from app.models.version import Version
from app.schemas.paper import PaperCreate, PaperUpdate
import uuid
from datetime import datetime

class PaperService:
    def __init__(self):
        # 这里应该是数据库连接，暂时使用内存存储
        self.papers = {}
        self.versions = {}  # 存储论文版本，格式：{paper_id: [version1, version2, ...]}
    
    def create_paper(self, paper_data: PaperCreate, user_id: str) -> Paper:
        paper_id = str(uuid.uuid4())
        paper = Paper(
            id=paper_id,
            title=paper_data.title,
            content=paper_data.content,
            outline=paper_data.outline,
            user_id=user_id,
            last_updated_by=user_id
        )
        self.papers[paper_id] = paper
        
        # 创建初始版本记录
        self._create_version(paper, user_id)
        
        return paper
    
    def get_papers(self, user_id: str) -> List[Paper]:
        return [paper for paper in self.papers.values() if paper.user_id == user_id]
    
    def get_paper(self, paper_id: str, user_id: str) -> Optional[Paper]:
        paper = self.papers.get(paper_id)
        if paper and paper.user_id == user_id:
            return paper
        return None
    
    def update_paper(self, paper_id: str, paper_data: PaperUpdate, user_id: str) -> Optional[Paper]:
        paper = self.get_paper(paper_id, user_id)
        if not paper:
            return None
        
        if paper_data.title is not None:
            paper.title = paper_data.title
        if paper_data.content is not None:
            paper.content = paper_data.content
        if paper_data.outline is not None:
            paper.outline = paper_data.outline
        
        paper.updated_at = datetime.utcnow()
        paper.last_updated_by = user_id
        self.papers[paper_id] = paper
        
        # 创建新版本记录
        self._create_version(paper, user_id)
        
        return paper
    
    def delete_paper(self, paper_id: str, user_id: str) -> bool:
        paper = self.get_paper(paper_id, user_id)
        if paper:
            del self.papers[paper_id]
            # 删除相关版本记录
            if paper_id in self.versions:
                del self.versions[paper_id]
            return True
        return False
    
    def _create_version(self, paper: Paper, user_id: str) -> Version:
        """创建版本记录"""
        if paper.id not in self.versions:
            self.versions[paper.id] = []
        
        version_number = len(self.versions[paper.id]) + 1
        version = Version(
            id=str(uuid.uuid4()),
            paper_id=paper.id,
            title=paper.title,
            content=paper.content,
            outline=paper.outline,
            created_by=user_id,
            version_number=version_number
        )
        
        self.versions[paper.id].append(version)
        return version
    
    def get_versions(self, paper_id: str, user_id: str) -> List[Version]:
        """获取论文的版本历史"""
        paper = self.get_paper(paper_id, user_id)
        if not paper:
            return []
        
        return self.versions.get(paper_id, [])
    
    def get_version(self, paper_id: str, version_id: str, user_id: str) -> Optional[Version]:
        """获取特定版本"""
        paper = self.get_paper(paper_id, user_id)
        if not paper:
            return None
        
        versions = self.versions.get(paper_id, [])
        for version in versions:
            if version.id == version_id:
                return version
        return None
    
    def rollback_to_version(self, paper_id: str, version_id: str, user_id: str) -> Optional[Paper]:
        """回滚到指定版本"""
        paper = self.get_paper(paper_id, user_id)
        if not paper:
            return None
        
        version = self.get_version(paper_id, version_id, user_id)
        if not version:
            return None
        
        # 更新论文内容为指定版本
        paper.title = version.title
        paper.content = version.content
        paper.outline = version.outline
        paper.updated_at = datetime.utcnow()
        paper.last_updated_by = user_id
        
        self.papers[paper_id] = paper
        
        # 创建新的版本记录（回滚操作本身也作为一个版本）
        self._create_version(paper, user_id)
        
        return paper
