package ms_core.repositories;

import ms_core.models.Job;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface AnalysisJobRepo extends JpaRepository<Job, UUID>{
}
